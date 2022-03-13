from django.shortcuts import render
from django.views import generic
from .models import *
import json


# Convert RawQuerySet to string in json format for javascript parsing

def raw_to_json(*RawQuerySets):
    array = []
    for set in RawQuerySets:
        for item in set:
            array.append({field:getattr(item,field) for field in set.columns})
    return json.dumps(array)


# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'm3di/index.html'

def main_UniVar(request):
    if request.method == "GET":
        query_uni = request.GET['q']
        query_var = request.GET['v']
        # obtain interaction score threshold
        if request.GET['s'] != 'Custom':
            query_sco = request.GET['s']
        else:
            query_sco = request.GET['s_custom']
        # obtain max number of iteractors
        if request.GET['l'] != 'Custom':
            query_lim = request.GET['l']
        else:
            query_lim = request.GET['l_custom']


    results_basic = Basicinfo2.objects.filter(uniprot_id__icontains=query_uni)
    results_signal = Signalpeptide.objects.filter(sp_uniprot_id__icontains=query_uni)
    # results_loc_cellcomp = Topocellcomp.objects.filter(uniprot_id__icontains=query_uni)
    # Pfam_results_general = Pfam.objects.filter(pf_uniprot_id__icontains=query_uni)
    # function_results = Proteinfunctionl.objects.filter(uniprot_id__icontains=query_uni)


    # results_signal = Signalpeptide.objects.raw(
    #     f'''SELECT * FROM ProNameUnique LEFT JOIN SignalPeptide 
    #     ON uniprot_id=sp_uniprot_id WHERE uniprot_id = "{query_uni}"''')

    if query_uni and query_var:

        results_variant = MissenseVarCom.objects.raw(
            'SELECT * FROM Missense_Var_Com WHERE uniprot = %s and posuniprot = %s', [
                query_uni, query_var])
        results_topo = Topodom.objects.raw(
        '''SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot = %s) AS tab 
        WHERE topo_start <= %s and topo_end >= %s''', [query_uni, query_var, query_var])

    elif query_uni:
        results_variant = MissenseVarCom.objects.raw(
            'SELECT * FROM Missense_Var_Com WHERE uniprot = %s LIMIT 10', [
                query_uni])
        results_topo = Topodom.objects.none()


    else:
        results_variant = MissenseVarCom.objects.none()



    cyNodes_raw = Stringinteractions.objects.raw('''
        SELECT * FROM BasicInfo2 WHERE uniprot_id = %s
        UNION
        (SELECT b.* FROM StringInteractions as s
        LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
        LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
        LEFT JOIN BasicInfo2 as b ON b.uniprot_id = su2.uniprot_id
        WHERE su1.uniprot_id = %s
            AND su2.uniprot_id IS NOT NULL 
            AND s.experimental >= %s
        ORDER BY s.experimental desc, s.combined_score, s.id 
        LIMIT %s);
        ''',[query_uni,query_uni,float(query_sco)*1000,int(query_lim)])

    # Use a list as an SQL parameter in Python:
    # Call tuple(list) to convert the list into a tuple object.
    # Call str.format(tuple) to format the SQL query str with the tuple from the previous step.
    nodes = tuple([obj.uniprot_id for obj in cyNodes_raw])

    cyEdges_raw = Stringinteractions.objects.raw('''
        SELECT s.id, su1.uniprot_id AS p1, su2.uniprot_id AS p2,
            s.experimental, i.type, i.PDB_id
        FROM StringInteractions as s
        LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
        LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
        LEFT JOIN interactome3D_1 as i ON i.prot1 = su2.uniprot_id 
            AND i.prot2 = su1.uniprot_id      
        WHERE su1.uniprot_id in {} 
            AND su2.uniprot_id in {}
            AND su1.uniprot_id > su2.uniprot_id
            AND experimental > 0;
        '''.format(nodes,nodes))        

    cyEdges_raw_self = Stringinteractions.objects.raw('''
        SELECT i.id, i.prot1 AS p1, i.prot2 AS p2, i.type, 
                i.PDB_id, 'y' as self
        FROM interactome3D_1 as i
        WHERE i.prot1 in {} AND i.prot2 in {} AND i.prot1 = i.prot2;
        '''.format(nodes,nodes))


    if query_var: 
        cyNodes_raw = Basicinfo2.objects.raw('''
        SELECT id, uniprot_id, protein_link, protein_name, gene_name, pos
        FROM (
            SELECT * 
            FROM BasicInfo2 WHERE uniprot_id in {}
            ) t1
        LEFT JOIN (
            SELECT uniprot_p2 AS uniprot_p2, GROUP_CONCAT(pos_p2,aa_p2 SEPARATOR ', ') AS pos
            FROM InteractionSurfaceFinal
            WHERE uniprot_p1 = %s AND uniprot_p2 in {}
            AND pos_p1 = %s
            GROUP BY uniprot_p2
            ) t2
        ON t1.uniprot_id = t2.uniprot_p2;
        '''.format(nodes,nodes),[query_uni,query_var])

    
    cyNodes_json = raw_to_json(cyNodes_raw)
    cyEdges_json = raw_to_json(cyEdges_raw, cyEdges_raw_self)

    context = {
        'query_uni': query_uni,
        'query_var': query_var,
        'results_basic': results_basic,
        'results_signal': results_signal,
        'results_topo': results_topo,
        'results_variant': results_variant,
        'cyEdges_json': cyEdges_json,
        'cyNodes_json': cyNodes_json
    }

    return render(request, 'm3di/main.html', context)



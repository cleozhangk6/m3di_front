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


        cyEdges_raw = Stringinteractions.objects.raw(
            '''WITH t AS 
                    (SELECT s.id, su1.uniprot_id AS p1, su2.uniprot_id AS p2, 
                            s.experimental, i.type, i.PDB_id
                    FROM StringInteractions as s
                    LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
                    LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
                    LEFT JOIN interactome3D_1 as i ON i.prot1 = su1.uniprot_id 
                        AND i.prot2 = su2.uniprot_id  
                    WHERE su1.uniprot_id = %s
                        AND su2.uniprot_id IS NOT NULL
                        AND s.experimental > 0
                    ORDER BY s.combined_score desc, s.id LIMIT 10)
                SELECT * FROM t
                UNION ALL
                (SELECT s.id, su1.uniprot_id AS p1, su2.uniprot_id AS p2,
                        s.experimental, i.type, i.PDB_id
                    FROM StringInteractions as s
                    LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
                    LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
                    LEFT JOIN interactome3D_1 as i ON i.prot1 = su2.uniprot_id 
                        AND i.prot2 = su1.uniprot_id      
                    WHERE su1.uniprot_id in (select p2 from t) 
                        AND su2.uniprot_id in (select p2 from t)
                        AND su1.uniprot_id > su2.uniprot_id
                        AND experimental > 0);''', [query_uni])

        cyNodes_raw = Stringinteractions.objects.raw('''
                SELECT * FROM BasicInfo2 WHERE uniprot_id = %s
                UNION
                (SELECT b.* FROM StringInteractions as s
                LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
                LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
                LEFT JOIN BasicInfo2 as b ON b.uniprot_id = su2.uniprot_id
                WHERE su1.uniprot_id = %s
                    AND su2.uniprot_id IS NOT NULL AND s.experimental > 0
                ORDER BY s.combined_score desc, s.id 
                LIMIT 10);''',[query_uni,query_uni])

        face = Stringinteractions.objects.raw('''
        WITH t AS (SELECT uniprot_id FROM BasicInfo2 WHERE uniprot_id = %s
        UNION
        (SELECT b.uniprot_id FROM StringInteractions as s
        LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
        LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
        LEFT JOIN BasicInfo2 as b ON b.uniprot_id = su2.uniprot_id
        WHERE su1.uniprot_id = %s AND su2.uniprot_id IS NOT NULL AND s.experimental > 0
        ORDER BY s.combined_score desc, s.id
        limit 10))
        SELECT DISTINCT uniprot_2, pos_p2
        FROM InteractionSurfaceAP
        WHERE uniprot_1 = %s AND uniprot_2 in (select * from t) AND pos_p1 =226;''',[query_uni,query_uni,query_uni])

        
        
        cyNodes_json = raw_to_json(cyNodes_raw)
        cyEdges_json = raw_to_json(cyEdges_raw)

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



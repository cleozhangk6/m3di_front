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


# Create Views

class IndexView(generic.TemplateView):
    template_name = 'm3di/index.html'

class DocView(generic.TemplateView):
    template_name = 'm3di/doc.html'

class StatsView(generic.TemplateView):
    template_name = 'm3di/stats.html'

class ContactView(generic.TemplateView):
    template_name = 'm3di/contact.html'

def main_UniVar(request):
    if request.method == "GET":
        # Obtain UniProt or gene ID
        query = request.GET['q']
        # Obtain residue position of variant        
        query_var = request.GET['v']
        # Obtain interaction score threshold
        if request.GET['s'] != 'Custom':
            query_sco = request.GET['s']
        else:
            query_sco = request.GET['s_custom']
        # Obtain max number of iteractors
        if request.GET['l'] != 'Custom':
            query_lim = request.GET['l']
        else:
            query_lim = request.GET['l_custom']

    if query:
        # Allow both UniProt and Gene ID input
        results_basic = Basicinfo2.objects.raw('SELECT * FROM BasicInfo2 WHERE uniprot_id=%s OR gene_name=%s', [query,query])
        # Convert query to UniProtID only
        query_uni = results_basic[0].uniprot_id

        results_protein = Pronameunique.objects.raw(
            'SELECT * FROM ProNameUnique join ProteinLink on ProNameUnique.uniprot_id = ProteinLink.uniprot_id where ProNameUnique.uniprot_id = %s' , [query_uni]
        )

        results_gene = Geneinfo.objects.raw(
            'SELECT * from GeneInfo where uniprot_id = %s', [query_uni]
        )

        results_loc_cellcomp = Topocellcomp.objects.raw( 
            'SELECT * from TopoCellComp where uniprot_id = %s', [query_uni]
        )

        results_loc_topolabel = Topocellcomp.objects.raw(
            'SELECT * FROM TopoCellComp where uniprot_id = %s AND topo_label IS NOT NULL', [query_uni]
        )

        results_signal = Signalpeptide.objects.raw(
            'SELECT * FROM SignalPeptide where uniprot_id = %s', [query_uni]
        )

        Pfam_results_general = Pfam.objects.raw(
            'SELECT * FROM Pfam WHERE  uniprot_id = %s ', [query_uni]
        )
        
        function_results = Proteinfunctionl.objects.raw(
            'SELECT * FROM ProteinFunctionl where uniprot_id = %s', [query_uni]
        )

        tm_results = Transmem.objects.raw(
            'SELECT * from TransMem join EviCodes on TransMem.eco = EviCodes.eco where uniprot_id = %s order by tm_start', [query_uni]
        )

        topo1_results = Topodom.objects.raw(
            'select * from TopoDom join EviCodes on TopoDom.eco = EviCodes.eco where uniprot_id = %s order by topo_start', [query_uni]
        )

        bind1_results = Bindsite.objects.raw(
            'select * from BindSite  join EviCodes on BindSite.eco = EviCodes.eco where uniprot_id = %s order by bs_position', [query_uni]
        )

        ptm1_results = Ptms.objects.raw(
            'select * from PTMs join EviCodes on PTMs.eco = EviCodes.eco where uniprot_id = %s ' , [query_uni]
        )

        var_results =  Missensevarcom.objects.raw(
            'SELECT * FROM MissenseVarCom WHERE uniprot_id = %s ' , [query_uni]
            )
    

        if query_uni and query_var is not None : 

            results_signal_var = Signalpeptide.objects.raw(
            'SELECT * FROM SignalPeptide where uniprot_id = %s and signal_peptide > %s ', [query_uni, query_var]
            )   

            trans_dom_var = Transmem.objects.raw(
            'SELECT * FROM TransMem where tm_start <= %s AND tm_end >= %s AND uniprot_id = %s ', [query_var, query_var, query_uni]
            )
        
            results_binding = Bindsite.objects.raw( 
            'SELECT * from BindSite join EviCodes on BindSite.eco = EviCodes.eco where uniprot_id = %s and bs_position = %s ', [query_uni, query_var]
            )

            results_topo = Topodom.objects.raw(
            '''SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot_id = %s) AS tab 
            WHERE topo_start <= %s and topo_end >= %s''', [
                query_uni, query_var, query_var]
            )
            results_variant = Missensevarcom.objects.raw(
            'SELECT * FROM MissenseVarCom WHERE uniprot_id = %s AND  posuniprot = %s' , [query_uni, query_var]
            )
            
            results_PTM = Ptms.objects.raw(
            'SELECT * FROM PTMs WHERE uniprot_id = %s AND pos = %s ' , [query_uni, query_var]
            )

            results_sequence = Seqcanonical.objects.raw( 
            'SELECT * FROM (SELECT id,  SUBSTRING(sequence, %s, 1) AS sub  FROM SeqCanonical where uniprot_id = %s) AS wt JOIN aa_conversion on wt.sub = aa_conversion.one_let' , [query_var, query_uni]
            )

            Pfam_results = Pfam.objects.raw(
            'SELECT * FROM Pfam WHERE ali_s  <= %s AND ali_e >= %s AND uniprot_id = %s ', [query_var, query_var, query_uni]
            )

        elif query_uni :

            results_variant = Missensevarcom.objects.raw(
                'SELECT * FROM MissenseVarCom WHERE uniprot_id = %s', [
                    query_uni]
            )


        # Return a list of nodes (interactors) for cytoscape
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

        # Avoid error caused by trailing comma in a single-item tuple (no interactors)
        if len(nodes) > 1:
            cyEdges_raw = Stringinteractions.objects.raw('''
                SELECT s.id, su1.uniprot_id AS p1, su2.uniprot_id AS p2,
                    s.experimental, i.type, i.PDB_id
                FROM StringInteractions as s
                LEFT JOIN StringToUniprot as su1 ON su1.string_id = s.string_p1
                LEFT JOIN StringToUniprot as su2 ON su2.string_id = s.string_p2
                LEFT JOIN Interactome3d as i ON i.prot1 = su2.uniprot_id 
                    AND i.prot2 = su1.uniprot_id      
                WHERE su1.uniprot_id in {} 
                    AND su2.uniprot_id in {}
                    AND su1.uniprot_id > su2.uniprot_id;
                '''.format(nodes,nodes))        
            cyEdges_raw_self = Stringinteractions.objects.raw('''
                SELECT i.id, i.prot1 AS p1, i.prot2 AS p2, i.type, 
                        i.PDB_id, 'y' as self
                FROM Interactome3d as i
                WHERE i.prot1 in {} AND i.prot2 in {} AND i.prot1 = i.prot2;
                '''.format(nodes,nodes))
            cyEdges_json = raw_to_json(cyEdges_raw, cyEdges_raw_self)
        else:
            cyEdges_json = None

        # Change cyNodes content (add interface info) when a variant is specified
        if query_var and len(nodes) > 1: 
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

        context = {
            'query': query,            
            'query_uni': query_uni,
            'query_var': query_var,
            'query_sco': query_sco,
            'query_lim': query_lim,
            'results_basic': results_basic,
            'cyNodes_json': cyNodes_json,
            'cyEdges_json': cyEdges_json,
            'nodes_len': len(nodes),
            'results_protein' : results_protein, 
            'results_gene': results_gene, 
            'results_signal' : results_signal,
            'results_signal_var' : results_signal_var,
            'trans_dom_var' : trans_dom_var,
            'tm_results' : tm_results, 
            'results_topo': results_topo,
            'results_loc_cellcomp' : results_loc_cellcomp, 
            'results_loc_topolabel': results_loc_topolabel,
            'results_variant': results_variant,
            'results_binding': results_binding, 
            'results_PTM': results_PTM,
            'Pfam_results' : Pfam_results,
            'Pfam_results_general': Pfam_results_general,
            'results_sequence': results_sequence,
            'function_results': function_results,
            'topo1_results' : topo1_results ,
            'bind1_results': bind1_results,
            'ptm1_results': ptm1_results,
            'var_results' :var_results
        }
    else:
        context = None

    return render(request, 'm3di/main.html', context)



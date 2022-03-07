from django.shortcuts import render
from django.views import generic
from .models import *
from itertools import chain

# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'basic/home.html'


class IndexView(generic.TemplateView):
    template_name = 'basic/index.html'

# class SearchView(generic.ListView):
#     template_name = 'basic/search.html'

#     def get_queryset(self): #overwrite the get_queryset method
#         query = self.request.GET.get('q', None)

#         if query is not None:
#             proname_results = Pronameunique.objects.filter(uniprot_id__icontains=query)
#             sigpep_results = Sigpep.objects.filter(sp_uniprot_id__icontains=query)
#             basicinfo_results = Basicbackup.objects.filter(uniprot_id__icontains=query)

#             # combine querysets
#             queryset_chain = chain(
#                 proname_results,
#                 sigpep_results,
#                 basicinfo_results
#             )

#             return queryset_chain
#         return ProNameUnique.objects.none()
# testinggit123


# class SearchView(generic.ListView):
#     template_name = 'basic/search.html'

#     def get_queryset(self):  # overwrite the get_queryset method
#         query = self.request.GET.get('q', None)

#         if query is not None:
#             basic_results = Basicinfo2.objects.raw(
#                 'SELECT * FROM BasicInfo2 LEFT JOIN SignalPeptide ON uniprot_id=sp_uniprot_id WHERE uniprot_id = %s', [query])

#             return basic_results
#         return Basicinfo2.objects.none()

def search_view(request):
    if request.method == "GET":
        query_uni = request.GET['q']
        query_var = request.GET['v']

        results_basic = Basicinfo2.objects.raw(
            'SELECT * FROM BasicInfo2 LEFT JOIN SignalPeptide ON uniprot_id=sp_uniprot_id WHERE uniprot_id = %s', [
                query_uni]
        )
        results_topo = Topodom.objects.raw(
            'SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot = %s) AS tab WHERE topo_start <= %s and topo_end >= %s', [
                query_uni, query_var, query_var]
        )
        results_variant = MissenseVarCom.objects.raw(
            'SELECT * FROM Missense_Var_Com WHERE uniprot = %s and posuniprot = %s', [
                query_uni, query_var]
        )
        context = {
            'results_basic': results_basic,
            'results_topo': results_topo,
            'results_variant': results_variant}

        return render(request, 'basic/search.html', context)

# class MainView(generic.ListView):
#     template_name = 'basic/main.html'

#     def get_queryset(self):  # overwrite the get_queryset method
#         query_uniprot = self.request.GET.get('q', None)
#         query_residue = self.request.GET.get('q2', None)

#         if query_uniprot is not None:
#             basic_results = Basicinfo2.objects.raw(
#                 'SELECT * FROM BasicInfo2 LEFT JOIN SignalPeptide ON uniprot_id=sp_uniprot_id WHERE uniprot_id = %s', [query_uniprot])

#             return basic_results
#         return Basicinfo2.objects.none()


def main_UniVar(request):
    if request.method == "GET":
        query_uni = request.GET['q']
        query_var = request.GET['v']

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
            'SELECT * FROM SignalPeptide where sp_uniprot_id = %s', [query_uni]
        )

        Pfam_results_general = Pfam.objects.raw(
            'SELECT * FROM Pfam WHERE  pf_uniprot_id = %s ', [query_uni]
        )
        
        function_results = Proteinfunctionl.objects.raw(
            'SELECT * FROM ProteinFunctionL where uniprot_id = %s', [query_uni]
        )

        tm_results = Transmem.objects.raw(
            'SELECT * from TransMem join EviCodes on TransMem.eco = EviCodes.eco where tm_uniprot_id = %s order by tm_start', [query_uni]
        )

        topo1_results = Topodom.objects.raw(
            'select * from TopoDom join EviCodes on TopoDom.eco = EviCodes.eco where uniprot = %s order by topo_start', [query_uni]
        )

        bind1_results = Bindsite.objects.raw(
            'select * from BindSite  join EviCodes on BindSite.eco = EviCodes.eco where uniprot_id = %s order by bs_position', [query_uni]
        )

        ptm1_results = Ptms.objects.raw(
            'select * from PTMs join EviCodes on PTMs.eco = EviCodes.eco where ptm_uniprot_id = %s ' , [query_uni]
        )
    

        if query_uni and query_var: 

            results_signal_var = Signalpeptide.objects.raw(
            'SELECT * FROM SignalPeptide where sp_uniprot_id = %s and signal_peptide > %s ', [query_uni, query_var]
            )   

            trans_dom_var = Transmem.objects.raw(
            'SELECT * FROM TransMem where tm_start <= %s AND tm_end >= %s AND tm_uniprot_id = %s ', [query_var, query_var, query_uni]
            )
        
            results_binding = Bindsite.objects.raw( 
            'SELECT * from BindSite join EviCodes on BindSite.eco = EviCodes.eco where uniprot_id = %s and bs_position = %s ', [query_uni, query_var]
            )

            results_topo = Topodom.objects.raw(
            '''SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot = %s) AS tab 
            WHERE topo_start <= %s and topo_end >= %s''', [
                query_uni, query_var, query_var]
            )
            results_variant = MissenseVarCom.objects.raw(
            'SELECT * FROM Missense_Var_Com WHERE uniprot = %s AND  posuniprot = %s' , [query_uni, query_var]
            )
            
            results_PTM = Ptms.objects.raw(
            'SELECT * FROM PTMs WHERE ptm_uniprot_id = %s AND pos = %s ' , [query_uni, query_var]
            )

            results_sequence = SeqCanonical.objects.raw( 
            'SELECT id, SUBSTRING(sequence, %s, 1) as wt FROM Seq_canonical where uniprot_id = %s' , [query_var, query_uni]
            )

            Pfam_results = Pfam.objects.raw(
            'SELECT * FROM Pfam WHERE env_s  <= %s AND env_e >= %s AND pf_uniprot_id = %s ', [query_var, query_var, query_uni]
            )

        elif query_uni :

            results_variant = MissenseVarCom.objects.raw(
                'SELECT * FROM Missense_Var_Com WHERE uniprot = %s', [
                    query_uni]
            )

        results_interact = Stringinteractions.objects.raw(
            '''SELECT id, s.string_p1, a.uniprot_id as uniprot_p1, s.string_p2, b.uniprot_id as uniprot_p2, experimental, data_base, combined_score, Json_object('uniprot_p1', a.uniprot_id, 'uniprot_p2',  b.uniprot_id) AS col_json
                FROM StringInteractions as s
                LEFT JOIN StringToUniprot as a
                ON a.string_id = s.string_p1
                LEFT JOIN StringToUniprot as b
                ON b.string_id = s.string_p2
                WHERE a.uniprot_id = %s
                AND b.uniprot_id IS NOT NULL AND experimental > 0
                ORDER BY s.combined_score
                limit 10;''', [query_uni]
        )

        results_interact_additional = Stringinteractions.objects.raw(
            '''WITH t as (SELECT b.uniprot_id as uniprot_p2
                FROM StringInteractions as s
                LEFT JOIN StringToUniprot as a
                ON a.string_id = s.string_p1
                LEFT JOIN StringToUniprot as b
                ON b.string_id = s.string_p2
                WHERE a.uniprot_id = %s
                AND b.uniprot_id IS NOT NULL
                AND experimental > 0
                ORDER BY s.combined_score
                limit 10)
                SELECT id, u.string_p1, c.uniprot_id as uniprot_p1, u.string_p2, d.uniprot_id as uniprot_p2, u.experimental, u.data_base, u.combined_score, 
                Json_object('uniprot_p1', c.uniprot_id, 'uniprot_p2',  d.uniprot_id) AS col_json_additional
                FROM StringInteractions as u
                LEFT JOIN StringToUniprot as c
                ON c.string_id = u.string_p1
                LEFT JOIN StringToUniprot as d
                ON d.string_id = u.string_p2
                WHERE c.uniprot_id in (select * from t) AND d.uniprot_id in (select * from t);''', [query_uni]
        )

        results_interact_list = []
        for item in results_interact:
            results_interact_list.append(item.col_json)
        for item in results_interact_additional:
            results_interact_list.append(item.col_json_additional)
        results_interact_string = '{"interactors": [' + \
            ",".join(results_interact_list) + ']}'
        

        context = {
            'query_uni': query_uni,
            'query_var': query_var,
            'results_protein' : results_protein, 
            'results_gene': results_gene, 
            'results_signal': results_signal,
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
            'results_interact_string': results_interact_string
        }

        return render(request, 'basic/main.html', context)

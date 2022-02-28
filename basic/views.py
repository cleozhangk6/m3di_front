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
        # results_topo = Topodom.objects.raw(
        #     'SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot = %s) AS tab WHERE topo_start <= %s and topo_end >= %s', [
        #         query_uni, query_var, query_var]
        # )
        results_variant = MissenseVarCom.objects.raw(
            'SELECT * FROM Missense_Var_Com WHERE uniprot = %s and posuniprot = %s', [query_uni, query_var]
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

        results_basic = Basicinfo2.objects.raw(
            'SELECT * FROM BasicInfo2 WHERE uniprot_id = %s', [query_uni]
        )

        

        results_topo = Topodom.objects.raw(
            '''SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot = %s) AS tab 
            WHERE topo_start <= %s and topo_end >= %s''', [
                query_uni, query_var, query_var]
        )

        if query_uni and query_var:

            results_variant = MissenseVarCom.objects.raw(
                'SELECT * FROM Missense_Var_Com WHERE uniprot = %s and posuniprot = %s', [
                    query_uni, query_var]
            )

            results_signal = Signalpeptide.objects.raw(
               '''SELECT sp_uniprot_id, pos, CASE WHEN pos >= %s THEN \'true\' ELSE \'false\' END FROM 
               (SELECT sp_uniprot_id, signal_peptide as pos 
               from SignalPeptide WHERE sp_uniprot_id = %s) AS tab;''', [query_var, query_uni]
            )

            results_transmem = Transmem.objects.raw(
                '''SELECT * from TransMem WHERE tm_uniprot_id = %s AND tm_start <= %s AND tm_end >= %s 
            ;''', [query_uni, query_var, query_var]
            )


        elif query_uni:
            results_variant = MissenseVarCom.objects.raw(
                'SELECT * FROM Missense_Var_Com_Copy WHERE uniprot = %s', [
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
                WHERE c.uniprot_id in (select * from t) AND d.uniprot_id in (select * from t) AND c.uniprot_id > d.uniprot_id;''', [query_uni]
        )

        # need to change to limit here, 100 is for testing
        results_interactome3d = Interactome3D1.objects.raw(
            '''
            SELECT id, prot1, prot2, type, PDB_id as pdb_id
            FROM interactome3D_1
            WHERE prot1 = %s OR prot2 =%s;
                ''', [query_uni,query_uni]
        )

         # ------This bit works (but querying from a denormalised table)-----
        # results_interact = StringInteractionUniprot.objects.raw(
        #     '''SELECT id, uniprot_p2, Json_object('uniprot_p1', uniprot_p1, 'uniprot_p2',  uniprot_p2) 
        #      AS col_json FROM string_interaction_uniprot WHERE uniprot_p1 = %s order by combined_score limit 10;''', [query_uni]
        # )

        # results_interact_additional = StringInteractionUniprot.objects.raw(
        #     '''WITH t AS (SELECT uniprot_p2 FROM string_interaction_uniprot WHERE uniprot_p1 = %s ORDER BY combined_score limit 10)
        #     SELECT id, Json_object('uniprot_p1', uniprot_p1, 'uniprot_p2',  uniprot_p2) AS col_json_additional FROM string_interaction_uniprot WHERE uniprot_p1 in (select * from t) and uniprot_p2 in (select * from t);''', [query_uni]
        # )
        #  ------This bit works-----

        # results_interact_list = []
        # for item in results_interact:
        #     results_interact_list.append('{\'p1\','+str(item.uniprot_p1)+',\'p2\','+ str(item.uniprot_p2)+'}')

        # results_interact_string = '{"interactors": [' + \
        #     ",".join(results_interact_list) + ']}'
        
        # results_interact = Pronameunique.objects.raw(
        #     """SELECT uniprot_p1, uniprot_p2, id, Json_object('uniprot_p1', uniprot_p1, 'uniprot_p2',  uniprot_p2) 
        #     AS col_json FROM ProNameUnique LEFT JOIN string_interaction_uniprot 
        #     ON uniprot_id=uniprot_p1 WHERE uniprot_id = %s LIMIT 10""", [
        #         query_uni]
        # )
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
            'results_basic': results_basic,
            'results_signal': results_signal,
            'results_topo': results_topo,
            'results_variant': results_variant,
            'results_interact_string': results_interact_string,
            'results_transmem': results_transmem,
            'results_interactome3d': results_interactome3d
        }

        return render(request, 'basic/main.html', context)

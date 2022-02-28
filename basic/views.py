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

        results_basic = Basicinfo2.objects.raw(
            'SELECT * FROM BasicInfo2 WHERE uniprot_id = %s', [query_uni]
        )

        results_signal = Pronameunique.objects.raw(
            '''SELECT * FROM ProNameUnique LEFT JOIN SignalPeptide 
            ON uniprot_id=sp_uniprot_id WHERE uniprot_id = %s''', [
                query_uni]
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
        elif query_uni:
            results_variant = MissenseVarCom.objects.raw(
                'SELECT * FROM Missense_Var_Com WHERE uniprot = %s', [
                    query_uni]
            )
        else:
            results_variant = MissenseVarCom.objects.none()

        # results_interact = Pronameunique.objects.raw(
        #     """SELECT uniprot_id, id, Json_object('uniprot_p1', uniprot_p1, 'uniprot_p2',  uniprot_p2) 
        #     AS col_json FROM ProNameUnique LEFT JOIN string_interaction_uniprot 
        #     ON uniprot_id=uniprot_p1 WHERE uniprot_id = %s LIMIT 10""", [
        #         query_uni]
        # )
        # results_interact_list = []
        # for item in results_interact:
        #     results_interact_list.append(item.col_json)
        # results_interact_string = '{"interactors": [' + \
        #     ",".join(results_interact_list) + ']}'

        results_interact = Stringinteractions.objects.raw(
            '''SELECT id, 
                    s.string_p1, 
                    a.uniprot_id as uniprot_p1, 
                    s.string_p2, 
                    b.uniprot_id as uniprot_p2, 
                    experimental, 
                    data_base, 
                    combined_score, 
                    Json_object('p1', a.uniprot_id, 'p2', b.uniprot_id, 'exp', experimental) 
                    as col_json
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
            '''WITH t as 
                    (SELECT b.uniprot_id as uniprot_p2
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
                SELECT id, 
                    u.string_p1, 
                    c.uniprot_id as uniprot_p1, 
                    u.string_p2, 
                    d.uniprot_id as uniprot_p2, 
                    u.experimental, 
                    u.data_base,  
                    u.combined_score, 
                    Json_object('p1', c.uniprot_id, 'p2', d.uniprot_id, 'exp', u.experimental) 
                    AS col_json_additional
                FROM StringInteractions as u
                LEFT JOIN StringToUniprot as c
                    ON c.string_id = u.string_p1
                LEFT JOIN StringToUniprot as d
                    ON d.string_id = u.string_p2
                WHERE c.uniprot_id in (select * from t) 
                    AND d.uniprot_id in (select * from t)
                    AND c.uniprot_id > d.uniprot_id;''', [query_uni]
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
            'results_basic': results_basic,
            'results_signal': results_signal,
            'results_topo': results_topo,
            'results_variant': results_variant,
            'results_interact_string': results_interact_string
        }

        return render(request, 'basic/main.html', context)



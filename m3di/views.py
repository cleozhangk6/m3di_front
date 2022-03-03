from django.shortcuts import render
from django.views import generic
from .models import *
from itertools import chain

# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'm3di/index.html'



# class MainView(generic.ListView):
#     template_name = 'm3di/main.html'

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


        # results_basic = Basicinfo2.objects.raw(
        #     f'SELECT * FROM BasicInfo2 WHERE uniprot_id = "{query_uni}"'
        # )
        
        results_basic = Basicinfo2.objects.filter(uniprot_id__icontains=query_uni).values()

        results_signal = Signalpeptide.objects.raw(
            f'''SELECT * FROM ProNameUnique LEFT JOIN SignalPeptide 
            ON uniprot_id=sp_uniprot_id WHERE uniprot_id = "{query_uni}"''')



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


        results_interact = Stringinteractions.objects.raw(
            '''SELECT s.id, 
                    Json_object('p1', su1.uniprot_id,
                                'p2', su2.uniprot_id,
                                'exp', s.experimental,
                                'type', i.type,
                                'p1_gene', g1.gene_name, 
                                'p2_gene', g2.gene_name) 
                    as cyData
                FROM StringInteractions as s
                LEFT JOIN StringToUniprot as su1
                    ON su1.string_id = s.string_p1
                LEFT JOIN StringToUniprot as su2
                    ON su2.string_id = s.string_p2
                LEFT JOIN interactome3D_1 as i
                    ON i.prot1 = su1.uniprot_id AND i.prot2 = su2.uniprot_id
                LEFT JOIN GeneInfo as g1
                    ON g1.uniprot_id = su1.uniprot_id
                LEFT JOIN GeneInfo as g2
                    ON g2.uniprot_id = su2.uniprot_id
                WHERE su1.uniprot_id = %s
                    AND su2.uniprot_id IS NOT NULL AND s.experimental > 0
                ORDER BY s.combined_score desc
            limit 10;''', [query_uni]
        )

        results_interact_additional = Stringinteractions.objects.raw(
            '''WITH t as 
                    (SELECT stu2.uniprot_id as uniprot_p2
                    FROM StringInteractions as st
                    LEFT JOIN StringToUniprot as stu1
                        ON stu1.string_id = st.string_p1
                    LEFT JOIN StringToUniprot as stu2
                        ON stu2.string_id = st.string_p2
                    WHERE stu1.uniprot_id = %s
                        AND stu2.uniprot_id IS NOT NULL
                        AND st.experimental > 0
                    ORDER BY st.combined_score desc
                    limit 10)
                SELECT s.id, 
                        Json_object('p1', su1.uniprot_id, 
                                    'p2', su2.uniprot_id, 
                                    'exp', s.experimental,
                                    'type',i.type,
                                    'p1_gene', g1.gene_name, 
                                    'p2_gene', g2.gene_name)
                        AS cyData_additional
                    FROM StringInteractions as s
                    LEFT JOIN StringToUniprot as su1
                        ON su1.string_id = s.string_p1
                    LEFT JOIN StringToUniprot as su2
                        ON su2.string_id = s.string_p2
                    LEFT JOIN interactome3D_1 as i
                        ON i.prot1 = su2.uniprot_id AND i.prot2 = su1.uniprot_id
                    LEFT JOIN GeneInfo as g1
                        ON g1.uniprot_id = su1.uniprot_id
                    LEFT JOIN GeneInfo as g2
                        ON g2.uniprot_id = su2.uniprot_id        
                    WHERE su1.uniprot_id in (select * from t) 
                        AND su2.uniprot_id in (select * from t)
                        AND su1.uniprot_id > su2.uniprot_id
                        AND experimental > 0;''', [query_uni]
        )

        results_interact_list = []
        for item in results_interact:
            results_interact_list.append(item.cyData)
        for item in results_interact_additional:
            results_interact_list.append(item.cyData_additional)
        results_interact_string = '[' + \
            ",".join(results_interact_list) + ']'


        context = {
            'query_uni': query_uni,
            'query_var': query_var,
            'results_basic': results_basic,
            'results_signal': results_signal,
            'results_topo': results_topo,
            'results_variant': results_variant,
            'results_interact_string': results_interact_string
        }

        return render(request, 'm3di/main.html', context)



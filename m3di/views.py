from django.shortcuts import render
from django.views import generic
from .models import *
import json


# Convert RawQuerySet to json format string for javascript parsing

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


        cyEdges_raw = Stringinteractions.objects.raw(
            '''SELECT s.id,
                    su1.uniprot_id AS p1,
                    su2.uniprot_id AS p2,
                    s.experimental AS exp,
                    i.type AS type
                FROM StringInteractions as s
                LEFT JOIN StringToUniprot as su1
                    ON su1.string_id = s.string_p1
                LEFT JOIN StringToUniprot as su2
                    ON su2.string_id = s.string_p2
                LEFT JOIN interactome3D_1 as i
                    ON i.prot1 = su1.uniprot_id AND i.prot2 = su2.uniprot_id
                WHERE su1.uniprot_id = %s
                    AND su2.uniprot_id IS NOT NULL AND s.experimental > 0
                ORDER BY s.combined_score desc, s.id
            limit 10;''', [query_uni]
        )

        cyEdges_add_raw = Stringinteractions.objects.raw(
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
                    ORDER BY st.combined_score desc, st.id
                    limit 10)
                SELECT s.id, 
                        su1.uniprot_id AS p1,
                        su2.uniprot_id AS p2,
                        s.experimental AS exp,
                        i.type AS type
                    FROM StringInteractions as s
                    LEFT JOIN StringToUniprot as su1
                        ON su1.string_id = s.string_p1
                    LEFT JOIN StringToUniprot as su2
                        ON su2.string_id = s.string_p2
                    LEFT JOIN interactome3D_1 as i
                        ON i.prot1 = su2.uniprot_id AND i.prot2 = su1.uniprot_id      
                    WHERE su1.uniprot_id in (select * from t) 
                        AND su2.uniprot_id in (select * from t)
                        AND su1.uniprot_id > su2.uniprot_id
                        AND experimental > 0;''', [query_uni])

        cyNodes_raw = Stringinteractions.objects.raw('''
                SELECT b.id, b.uniprot_id AS uniprot, b.gene_name AS gene 
                    FROM BasicInfo2 AS b WHERE uniprot_id = %s
                UNION
                (SELECT s.id, su2.uniprot_id AS uniprot,
                        b.gene_name AS gene
                FROM StringInteractions as s
                LEFT JOIN StringToUniprot as su1
                    ON su1.string_id = s.string_p1
                LEFT JOIN StringToUniprot as su2
                    ON su2.string_id = s.string_p2
                LEFT JOIN BasicInfo2 as b
                    ON b.uniprot_id = su2.uniprot_id
                WHERE su1.uniprot_id = %s
                    AND su2.uniprot_id IS NOT NULL AND s.experimental > 0
                ORDER BY s.combined_score desc, s.id
                limit 10);''', [query_uni,query_uni])
        
        cyNodes_json = raw_to_json(cyNodes_raw)
        cyEdges_json = raw_to_json(cyEdges_raw, cyEdges_add_raw)

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



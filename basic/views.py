from django.shortcuts import render
from django.views import generic
from .models import *
from itertools import chain

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'basic/home.html'

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


class SearchView(generic.ListView):
    template_name = 'basic/search.html'

            
    def get_queryset(self): #overwrite the get_queryset method
        global query
        query = self.request.GET.get('q', None)
        global variant
        variant = self.request.GET.get('v', None)

        if query and variant is not None:

            
            global topo_results
            topo_results = Topodom.objects.raw(
                'SELECT id, topology FROM (SELECT * FROM TopoDom WHERE uniprot = %s) AS tab WHERE topo_start <= %s and topo_end >= %s', [query, variant, variant])
            global variant_results
            variant_results = MissenseVarCom.objects.raw(
                'SELECT * FROM Missense_Var_Com WHERE uniprot = %s and posuniprot = %s', [query, variant])
            
            final_results= list(chain(topo_results, variant_results))


            return  final_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topo_results"] = topo_results
        context["variant_results"] =variant_results
        return context

        return  Topodom.objects.none()





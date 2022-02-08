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
        query = self.request.GET.get('q', None)

        if query is not None:
            basic_results = Basicinfo2.objects.raw(
                'SELECT * FROM BasicInfo2 LEFT JOIN SigPepFin ON uniprot_id=sp_uniprot_id WHERE uniprot_id = %s', [query])

            return basic_results
        return Basicinfo2.objects.none()


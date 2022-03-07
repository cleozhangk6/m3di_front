from django.urls import path
from . import views
from basic.views import *

app_name = 'basic'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    # path('search/',SearchView.as_view(),name='search-results'),
    path('search/',views.search_view,name='search-results'),
    
    path('index/',IndexView.as_view(),name='index'),
    # path('index/main/',MainView.as_view(),name='main'),
    path('index/main/',views.main_UniVar,name='main'),


]




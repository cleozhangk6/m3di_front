from django.urls import path
from . import views
from basic.views import *

app_name = 'basic'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('search/',SearchView.as_view(),name='search-results'),
]
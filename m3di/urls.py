from django.urls import path
from . import views
from m3di.views import *

app_name = 'm3di'

urlpatterns = [    
    path('',IndexView.as_view(),name='index'),
    path('main/',views.main_UniVar,name='main'),
]




from django.urls import path
from . import views
from basic.views import *

app_name = 'basic'

urlpatterns = [    
    path('',IndexView.as_view(),name='index'),
    path('/main/',views.main_UniVar,name='main'),
]




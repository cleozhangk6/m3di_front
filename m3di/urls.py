from django.urls import path
from . import views
from m3di.views import *

app_name = 'm3di'

urlpatterns = [    
    path('',IndexView.as_view(),name='index'),
    path('main/',views.main_UniVar,name='main'),
    path('help/',HelpView.as_view(), name='help'),
    path('statistics/',StatisticsView.as_view(), name='statistics'),
    path('contact/',ContactView.as_view(), name='contact'),
    path('doc/',DocView.as_view(), name='doc')
]




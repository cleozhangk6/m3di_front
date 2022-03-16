from django.urls import path
from . import views
from m3di.views import *

app_name = 'm3di'

urlpatterns = [    
    path('',IndexView.as_view(),name='index'),
    # path('',views.index,name='index'),
    # path('main-uni/',views.main_Uni,name='main-uni'),
    path('main/',views.main_UniVar,name='main'),
    path('documentation/',DocView.as_view(),name='doc'),
    path('statistics/',StatsView.as_view(),name='stats'),
    path('contact/',ContactView.as_view(),name='contact'),
]




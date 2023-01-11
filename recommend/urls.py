from .views import *
from django.urls import path

app_name = 'reco'

urlpatterns = [
    path('', similar_problem, name='similar_problem'),
    path('compare/', compare, name='compare'),
]
from .views import *
from django.urls import path

app_name = 'search'

urlpatterns = [
    path('license_info/', license_info, name='license_info')
]
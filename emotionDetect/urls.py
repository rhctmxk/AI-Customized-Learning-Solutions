from .views import *
from django.urls import path

app_name = 'emotion'

urlpatterns = [
    path('VidFeed/', VidFeed, name='VidFeed'),

]
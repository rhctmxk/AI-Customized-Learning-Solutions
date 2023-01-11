from .views import *
from django.urls import path

app_name = 'note'

urlpatterns = [
    path('', note_main, name='note_main'),
    path('select_subject', select_subject, name='select_subject'),
    path('note_subject1', note_subject1, name='note_subject1'),
    path('note_subject2', note_subject2, name='note_subject2'),
    path('note_subject3', note_subject3, name='note_subject3'),
    path('note_subject4', note_subject4, name='note_subject4'),
    path('note_subject5', note_subject5, name='note_subject5'),
]
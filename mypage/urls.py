from .views import *
from django.urls import path

app_name = 'mypage'

urlpatterns = [
    path('', home, name='home'),
    path('delete_alert/', delete_alert, name='delete_alert'),
    path('my_subject1/', my_subject1, name='my_subject1'),
    path('my_subject2/', my_subject2, name='my_subject2'),
    path('my_subject3/', my_subject3, name='my_subject3'),
    path('my_subject4/', my_subject4, name='my_subject4'),
    path('my_subject5/', my_subject5, name='my_subject5'),
    path('studylicense/', studylicense, name='studylicense'),
    path('theoryVideo/', theoryVideo, name='theoryVideo'),
    path('license/', license, name='license'),
    path('add_license/', add_license, name='add_license'),
]
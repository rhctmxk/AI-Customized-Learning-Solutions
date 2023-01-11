from . import views
from .views import *

from django.urls import path, include

app_name = 'extest'

urlpatterns = [
    path("", studymain, name="studymain"),
    path("omrstart/", omrstart, name="omrstart"),
    path("abilitystart/", views.abilitystart, name="abilitystart"),
    path("abilitytest/", views.abilitytest, name="abilitytest"),
    path("previousstart/", views.previousstart, name="previousstart"),
    path("previoustest/", views.previoustest, name="previoustest"),
    path("submit_omr/", views.submit_omr, name="submit_omr"),
    path("cancle_omr/", views.cancle_omr, name="cancle_omr"),
    path("omrtest/", views.omrtest, name="omrtest"),
    path("test/", views.test, name="test"),
    path("omrtest/data_save/", views.data_save, name="data_save"),
    path("abilitytest/data_save/", views.data_save, name="data_save"),
    path("previoustest/data_save/", views.data_save, name="data_save"),
    path("result_omr/data_save/", views.data_save, name="data_save"),
    path("wrongstart/", views.wrongstart, name="wrongstart"),
    path("wrongtest/", views.wrongtest, name="wrongtest"),
    path("result_omr/", views.result_omr, name="result_omr"),
    path("wrongreview/", views.wrongreview, name="wrongreview"),
    path("wrongview/", views.wrongview, name="wrongview"),
    path("nonlogin_abilitystart/", views.nonlogin_abilitystart, name="nonlogin_abilitystart"),
]
from .views import *
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('email/', email, name='email'),
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('delete/', delete, name='delete'),
    path('member_modify/', member_modify, name='member_modify'),
    path('find_id/', find_id, name='find_id'),
    path('find_pw/', find_pw, name='find_pw'),
    path('change_pw/', change_pw, name='change_pw'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),
]
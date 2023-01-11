from .views import *
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('home/', home, name='home'),
    path('', homeBefore, name='homeBefore'),
    path('community/write', community_write, name='community_write'),
    path('community/<int:communityId>', community_read, name='community_read'),
    path('community/<int:communityId>/modify', community_modify, name='community_modify'),
    path('community/<int:communityId>/delete', community_delete, name='community_delete'),
    path('community/<int:communityId>/comment_write', community_comment_write,
         name='community_comment_write'),
    path('community/<int:communityId>/comment_delete/<int:commentId>', community_comment_delete,
         name='community_comment_delete'),
    path('community/<int:communityId>/download', community_download, name='community_download'),
]
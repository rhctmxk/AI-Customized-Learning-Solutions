from .views import *
from django.urls import path

app_name = 'group'

urlpatterns = [
    path('group/', group, name='group'),
    path('groupstudy/write', groupstudy_write, name='groupstudy_write'),
    path('groupstudy/<int:groupstudyId>', groupstudy_read, name='groupstudy_read'),
    path('groupstudy/<int:groupstudyId>/modify', groupstudy_modify, name='groupstudy_modify'),
    path('groupstudy/<int:groupstudyId>/delete', groupstudy_delete, name='groupstudy_delete'),
    path('groupstudy/<int:groupstudyId>/comment_write', groupstudy_comment_write,
         name='groupstudy_comment_write'),
    path('groupstudy/<int:groupstudyId>/comment_delete/<int:groupstudycommentId>', groupstudy_comment_delete,
         name='groupstudy_comment_delete'),
    path('groupstudy/<int:groupstudyId>/participate', groupstudy_group_participate,
         name='groupstudy_group_participate'),
    path('groupstudy/<int:groupstudyId>/departicipate', groupstudy_group_departicipate,
         name='groupstudy_group_departicipate'),
    path('group/<int:groupId>', group_read, name='group_read'),
    path('group/<int:groupId>/modify', group_modify, name='group_modify'),
    path('group/<int:groupId>/delete', group_delete, name='group_delete'),
    path('group/<int:groupId>/download', group_download, name='group_download'),
    path('group/<int:groupId>/group_user_manage', group_user_manage, name='group_user_manage'),
    path('group/<int:groupId>/boardwrite', group_board_write, name='group_board_write'),
    path('group/<int:groupId>/groupboard/<int:groupboardId>', group_board_read, name='group_board_read'),
    path('group/<int:groupId>/boardread/<int:groupboardId>/download', group_board_download,
         name='group_board_download'),
    path('group/<int:groupId>/boardread/<int:groupboardId>/delete', group_board_delete,
         name='group_board_delete'),
    path('group/<int:groupId>/boardread/<int:groupboardId>/modify', group_board_modify,
         name='group_board_modify'),
    path('group/<int:groupId>/group_comment_write/<int:groupboardId>', group_comment_write,
         name='group_comment_write'),
    path('group/<int:groupId>/group_comment_delete/<int:groupboardId>/<int:groupcommentId>',
         group_comment_delete, name='group_comment_delete')
 ]
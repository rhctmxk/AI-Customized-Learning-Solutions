from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import User
from main.models import Community, Comment
from group.models import GroupUser, GroupInfo, GroupBoard, GroupComment, GroupStudy, GroupStudyComment
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.


# 방 리스트
@login_required(login_url='accounts:login')
def group(request):
    current_user = request.user
    try:
        groupusers = GroupUser.objects.filter(userid=current_user, is_registered=True)
        boards = GroupStudy.objects.all()
    except:
        boards = GroupStudy.objects.all()
        return render(request, 'group/group.html', {'boards': boards})
    return render(request, 'group/group.html', {'groupusers': groupusers, 'boards': boards})


# 글쓰는 곳
@login_required(login_url='accounts:login')
def groupstudy_write(request):
    data = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')

        recruit_start = request.POST.get('recruitStartDate')
        recruit_end = request.POST.get('recruitEndDate')
        activity_start = request.POST.get('activityStartDate')
        activity_end = request.POST.get('activityEndDate')
        created_date = timezone.now()

        recruit_start_date = datetime.strptime(recruit_start, '%Y-%m-%d')
        recruit_end_date = datetime.strptime(recruit_end, '%Y-%m-%d')
        activity_start_date = datetime.strptime(activity_start, '%Y-%m-%d')
        activity_end_date = datetime.strptime(activity_end, '%Y-%m-%d')

        data = {'title': title, 'content': content, 'recruit_start': recruit_start,
                'recruit_end': recruit_end, 'activity_start': activity_start, 'activity_end': activity_end}

        if recruit_start_date > recruit_end_date:
            messages.warning(request, '모집 종료 일은 모집 시작 일 이후로 설정해야 합니다.')
        elif activity_start_date > activity_end_date:
            messages.warning(request, '활동 종료 일은 활동 시작 일 이후로 설정해야 합니다.')
        elif recruit_end_date > activity_start_date:
            messages.warning(request, '활동 시작 일은 모집 종료 일 이후로 설정해야 합니다.')
        elif len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')
        else:
            try:
                post_add = GroupStudy(userid=request.user, title=title, content=content,
                                     recruitment_start_date=recruit_start, recruitment_end_date=recruit_end,
                                     activity_start_date=activity_start, activity_end_date=activity_end,
                                     created_date=created_date)
                post_add.save()
                print('a')
                post_id = GroupStudy.objects.filter(userid=request.user).latest('pk_id')
                group_info_add = GroupInfo(mentorid=request.user, groupstudyid=post_id, title=title, content=content,
                                           recruitment_start_date=recruit_start,
                                           recruitment_end_date=recruit_end, activity_start_date=activity_start,
                                           activity_end_date=activity_end, created_date=created_date)
                group_info_add.save()
                print('b')
                group_info_id = GroupInfo.objects.filter(mentorid=request.user).latest('pk_id')
                group_user_add = GroupUser(userid=request.user, groupinfoid=group_info_id, is_waiting=False,
                                           is_registered=True)
                group_user_add.save()
                print('c')
                return redirect('group:group')
            except:
                print('d')
                messages.warning(request, '게시글 저장에 실패했습니다.')

    return render(request, 'group/groupstudywrite.html', data)


@login_required(login_url='accounts:login')
def groupstudy_read(request, groupstudyId):
    currentuser = request.user

    post = get_object_or_404(GroupStudy, pk_id=groupstudyId)
    comments = GroupStudyComment.objects.filter(groupstudyid=post.pk_id).order_by('-created_date')
    member = GroupUser.objects.filter(groupinfoid=groupstudyId, is_registered=1)
    if comments.count() == 0:
        comments = {}

    try:
        groupinfo = GroupInfo.objects.get(groupstudyid=post)
    except:
        groupinfo = None

    try:
        group = GroupUser.objects.get(groupinfoid=groupinfo, userid=currentuser)
    except:
        group = None

    is_waiting = GroupUser.objects.filter(groupinfoid=groupinfo, is_waiting=True)
    is_registered = GroupUser.objects.filter(groupinfoid=groupinfo, is_registered=True)

    return render(request, 'group/groupstudyread.html',
                  {'post': post, 'currentuser': currentuser, 'comments': comments, 'group': group,
                   'groupinfo': groupinfo, 'member':member, 'is_waiting': is_waiting, 'is_registered' : is_registered})


@login_required(login_url='accounts:login')
def groupstudy_modify(request, groupstudyId):
    post = GroupStudy.objects.get(pk_id=groupstudyId)
    data = {'pk_id': post.pk_id, 'title': post.title, 'content': post.content, 'recruit_start': post.recruitment_start_date,
            'recruit_end': post.recruitment_end_date, 'activity_start': post.activity_start_date, 'activity_end': post.activity_end_date}

    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')
        post.title = title

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')
        post.content = content

        recruit_start = request.POST.get('recruitStartDate')
        post.recruitment_start_date = recruit_start

        recruit_end = request.POST.get('recruitEndDate')
        post.recruitment_end_date = recruit_end

        activity_start = request.POST.get('activityStartDate')
        post.activity_start_date = activity_start

        activity_end = request.POST.get('activityEndDate')
        post.activity_end_date = activity_end

        recruit_start_date = datetime.strptime(recruit_start, '%Y-%m-%d')
        recruit_end_date = datetime.strptime(recruit_end, '%Y-%m-%d')
        activity_start_date = datetime.strptime(activity_start, '%Y-%m-%d')
        activity_end_date = datetime.strptime(activity_end, '%Y-%m-%d')

        data = {'pk_id': post.pk_id, 'title': title, 'content': content, 'recruit_start': recruit_start,
                'recruit_end': recruit_end, 'activity_start': activity_start, 'activity_end': activity_end}

        if recruit_start_date > recruit_end_date:
            messages.warning(request, '모집 종료 일은 모집 시작 일 이후로 설정해야 합니다.')
        elif activity_start_date > activity_end_date:
            messages.warning(request, '활동 종료 일은 활동 시작 일 이후로 설정해야 합니다.')
        elif recruit_end_date > activity_start_date:
            messages.warning(request, '활동 시작 일은 모집 종료 일 이후로 설정해야 합니다.')
        elif len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')
        else:
            post.save()
            return redirect('group:groupstudy_read', groupstudyId)

    return render(request, 'group/groupstudymodify.html', data)

@login_required(login_url='accounts:login')
def groupstudy_delete(request, groupstudyId):
    try:
        del_post = GroupStudy.objects.get(pk_id=groupstudyId)
        del_post.delete()
    except:
        return redirect('group: group')
    return redirect('group: group')

@login_required(login_url='accounts:login')
def groupstudy_comment_write(request, groupstudyId):
    content = request.POST.get('comment')
    created_date = timezone.now()
    post = GroupStudy.objects.get(pk_id=groupstudyId)

    valid_content = content.replace(' ', '').replace('\n', '')

    if len(valid_content) != 0:
        comment = GroupStudyComment.objects.create(groupstudyid=post, content=content, userid=request.user, created_date=created_date)
        comment.save()
    else:
        messages.warning(request, '공백 댓글은 입력할 수 없습니다.')

    return redirect('group:groupstudy_read', groupstudyId)

@login_required(login_url='accounts:login')
def groupstudy_comment_delete(request, groupstudyId, groupstudycommentId):
    try:
        del_comment = GroupStudyComment.objects.get(pk_id=groupstudycommentId)
        del_comment.delete()
    except:
        return redirect('group:groupstudy_read', groupstudyId)
    return redirect('group:groupstudy_read', groupstudyId)

@login_required(login_url='accounts:login')
def groupstudy_group_participate(request, groupstudyId):
    current_user = request.user
    post = get_object_or_404(GroupStudy, pk_id=groupstudyId)
    groupinfo = get_object_or_404(GroupInfo, groupstudyid=post)

    is_exists = GroupUser.objects.filter(userid=current_user, groupinfoid=groupinfo)
    if is_exists.count() == 0:
        group_add = GroupUser(userid=current_user, groupinfoid=groupinfo, is_waiting=True, is_registered=False)
        group_add.save()

    return redirect('group:groupstudy_read', groupstudyId)

@login_required(login_url='accounts:login')
def groupstudy_group_departicipate(request, groupstudyId):
    current_user = request.user
    post = get_object_or_404(GroupStudy, pk_id=groupstudyId)
    groupinfo = get_object_or_404(GroupInfo, groupstudyid=post)

    del_record = GroupUser.objects.filter(groupinfoid=groupinfo, userid=current_user)
    del_record.delete()

    return redirect('group:groupstudy_read', groupstudyId)

# 권한있는 사람들만 글 읽는 곳
@login_required(login_url='accounts:login')
def group_read(request, groupId):
    current_user = request.user

    groupinfo = GroupInfo.objects.get(pk_id=groupId)
    groupboards = GroupBoard.objects.filter(groupinfoid=groupinfo)
    is_waiting = GroupUser.objects.filter(groupinfoid=groupinfo, is_waiting=True)
    is_registered = GroupUser.objects.filter(groupinfoid=groupinfo, is_registered=True)

    if (is_registered.filter(userid=current_user)).count() == 0:
        messages.warning(request, '페이지 접근 권한이 없습니다.')
        return redirect('group')

    return render(request, 'group/read.html', {'groupinfo': groupinfo, 'is_waiting': is_waiting, 'is_registered': is_registered, 'current_user': current_user, 'groupboards': groupboards})

# 파일 다운로드
@login_required(login_url='accounts:login')
def group_download(request, groupId):
    post = GroupInfo.objects.get(pk_id=groupId)
    file_name = post.filepath.name
    file_path = post.filepath.path
    file_type = post.filetype
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

@login_required(login_url='accounts:login')
def group_modify(request, groupId):
    post = GroupInfo.objects.get(pk_id=groupId)
    data = {'pk_id': post.pk_id, 'title': post.title, 'content': post.content, 'recruit_start': post.recruitment_start_date,
            'recruit_end': post.recruitment_end_date, 'activity_start': post.activity_start_date, 'activity_end': post.activity_end_date}

    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')
        post.title = title

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')
        post.content = content



        recruit_start = request.POST.get('recruitStartDate')
        post.recruitment_start_date = recruit_start

        recruit_end = request.POST.get('recruitEndDate')
        post.recruitment_end_date = recruit_end

        activity_start = request.POST.get('activityStartDate')
        post.activity_start_date = activity_start

        activity_end = request.POST.get('activityEndDate')
        post.activity_end_date = activity_end

        recruit_start_date = datetime.strptime(recruit_start, '%Y-%m-%d')
        recruit_end_date = datetime.strptime(recruit_end, '%Y-%m-%d')
        activity_start_date = datetime.strptime(activity_start, '%Y-%m-%d')
        activity_end_date = datetime.strptime(activity_end, '%Y-%m-%d')

        data = {'pk_id': post.pk_id, 'title': title, 'content': content, 'recruit_start': recruit_start,
                'recruit_end': recruit_end, 'activity_start': activity_start, 'activity_end': activity_end}

        if recruit_start_date > recruit_end_date:
            messages.warning(request, '모집 종료 일은 모집 시작 일 이후로 설정해야 합니다.')
        elif activity_start_date > activity_end_date:
            messages.warning(request, '활동 종료 일은 활동 시작 일 이후로 설정해야 합니다.')
        elif recruit_end_date > activity_start_date:
            messages.warning(request, '활동 시작 일은 모집 종료 일 이후로 설정해야 합니다.')
        elif len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')
        else:
            post.save()
            return redirect('group:group_read', groupId)

    return render(request, 'group/modify.html', data)

@login_required(login_url='accounts:login')
def group_delete(request, groupId):
    try:
        del_post = GroupInfo.objects.get(pk_id=groupId)
        del_post.delete()
    except:
        return redirect('group:group')
    return redirect('group:group')

@login_required(login_url='accounts:login')
def group_user_manage(request, groupId):
    groupinfo = get_object_or_404(GroupInfo, pk_id=groupId)
    is_waiting = GroupUser.objects.filter(groupinfoid=groupinfo, is_waiting=True)
    is_registered = GroupUser.objects.filter(groupinfoid=groupinfo, is_registered=True)

    if request.method == 'POST':
        registeruser_id = request.POST.get('registerUser')
        rejectuser_id = request.POST.get('rejectUser')
        deleteuser_id = request.POST.get('deleteUser')
        mentoruser_id = request.POST.get('mentorUser')

        if registeruser_id != None:
            registeruser = is_waiting.get(userid=registeruser_id)
            registeruser.is_waiting = False
            registeruser.is_registered = True
            registeruser.save()
        elif rejectuser_id != None:
            rejectuser = is_waiting.get(userid=rejectuser_id)
            rejectuser.delete()
        elif deleteuser_id != None:
            deleteuser = is_registered.get(userid=deleteuser_id)
            deleteuser.delete()
        elif mentoruser_id != None:
            mentouser = User.objects.get(id=mentoruser_id)
            groupinfo.mentorid = mentouser
            groupinfo.save()

        return redirect('group:group_read', groupId)

@login_required(login_url='accounts:login')
def group_board_write(request, groupId):
    data = {'groupId': groupId}
    groupinfo = GroupInfo.objects.get(pk_id=groupId)
    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')

        created_date = timezone.now()

        filepath = request.FILES.get('filepath')
        if filepath != None:
            filetype = request.FILES.get('filepath').content_type
        else:
            filepath = ''
            filetype = ''

        data = {'title': title, 'content': content, 'filepath': filepath, 'filetype': filetype, 'groupId': groupId}

        if len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')

        else:
            try:
                post_add = GroupBoard(userid=request.user, groupinfoid=groupinfo, title=title, content=content, created_date=created_date, filepath=filepath, filetype=filetype, is_notice=False)
                post_add.save()

                return redirect('group:group_read', groupId)

            except:
                messages.warning(request, '게시글 저장에 실패했습니다.')

    return render(request, 'group/boardwrite.html', data)

@login_required(login_url='accounts:login')
def group_board_read(request, groupId, groupboardId):
    currentuser = request.user

    post = get_object_or_404(GroupBoard, pk_id=groupboardId)
    comments = GroupComment.objects.filter(groupboardid=post).order_by('-created_date')

    if comments.count() == 0:
        comments = {}

    return render(request, 'group/boardread.html', {'post': post, 'currentuser': currentuser, 'comments': comments, 'groupId': groupId})

@login_required(login_url='accounts:login')
def group_board_download(request, groupId, groupboardId):
    post = GroupBoard.objects.get(pk_id=groupboardId)
    file_name = post.filepath.name
    file_path = post.filepath.path
    file_type = post.filetype
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

@login_required(login_url='accounts:login')
def group_board_delete(request, groupId, groupboardId):
    try:
        del_post = GroupBoard.objects.get(pk_id=groupboardId)
        del_post.delete()
    except:
        messages.warning(request, '게시글 삭제에 실패했습니다.')
        return redirect('group:group_read', groupId)
    return redirect('group:group_read', groupId)

@login_required(login_url='accounts:login')
def group_board_modify(request, groupId, groupboardId):
    post = GroupBoard.objects.get(pk_id=groupboardId)
    data = {'title': post.title, 'content': post.content, 'filepath': post.filepath, 'filetype': post.filetype, 'groupId': groupId, 'groupboardId': groupboardId}

    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')
        post.title = title

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')
        post.content = content

        created_date = timezone.now()

        filepath = request.FILES.get('filepath')
        if filepath != None:
            post.filepath = filepath
            filetype = request.FILES.get('filepath').content_type
            post.filetype = filetype
        else:
            filepath = post.filepath
            filetype = post.filetype

        data = {'title': title, 'content': content, 'filepath': filepath, 'filetype': filetype, 'groupId': groupId, 'groupboardId': groupboardId}


        if len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')

        else:
            try:
                post.save()

                return redirect('group:group_board_read', groupId, groupboardId)

            except:
                messages.warning(request, '게시글 저장에 실패했습니다.')

    return render(request, 'group/boardmodify.html', data)

@login_required(login_url='accounts:login')
def group_comment_write(request, groupId, groupboardId):
    content = request.POST.get('comment')
    created_date = timezone.now()
    post = GroupBoard.objects.get(pk_id=groupboardId)

    valid_content = content.replace(' ', '').replace('\n', '')

    if len(valid_content) != 0:
        comment = GroupComment.objects.create(groupboardid=post, content=content, userid=request.user, created_date=created_date)
        comment.save()
    else:
        messages.warning(request, '공백 댓글은 입력할 수 없습니다.')

    return redirect('group:group_board_read', groupId, groupboardId)

@login_required(login_url='accounts:login')
def group_comment_delete(request, groupId, groupboardId, groupcommentId):
    try:
        del_comment = GroupComment.objects.get(pk_id=groupcommentId)
        del_comment.delete()
    except:
        return redirect('group:group_board_read', groupId, groupboardId)
    return redirect('group:group_board_read', groupId, groupboardId)

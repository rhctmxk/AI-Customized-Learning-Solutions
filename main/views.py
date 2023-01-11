from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Community, Comment, Review
from django.utils import timezone
from django.contrib import messages
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.apps import apps

# 로그인 전 메인화면
def homeBefore(request):
    reviews = Review.objects.all()
    License_raking = apps.get_model('search', 'License_raking')
    licenses = License_raking.objects.all()
    params = {'reviews': reviews,
              'licenses': licenses}
    return render(request, 'main/index.html', params)

# 로그인 후 메인화면
def home(request):
    boards = Community.objects.all()
    boardType = '전체'
    board_type = ''
    # 게시판 타입 버튼을 눌렀을 때, 어떤게시판인지 가져옴.
    if request.method == 'POST':
        board_type = request.POST.get('board_type')
        try:
            if board_type == 'notice':
                boards = Community.objects.filter(type='notice')
                boardType = '공지사항'
            elif board_type == 'exam_info':
                boards = Community.objects.filter(type='exam_info')
                boardType = '시험정보'
            elif board_type == 'previous_question':
                boards = Community.objects.filter(type='previous_question')
                boardType = '기출문제'
            elif board_type == 'question':
                boards = Community.objects.filter(type='question')
                boardType = '이용 Q&A'
        except:
            print("error")

    # 게시판 검색기능
    if 'search' in request.POST:
        search = request.POST.get('search') #
        search_type = request.POST.get('search_type') # 전체, 제목+내용 등등을 고르는
        boardType = '\'' + str(search) + '\'' + "에 대한 검색 결과 입니다."


        try:
            if search_type == 'all':
                user_id = User.objects.get(first_name=search).id
                boards = Community.objects.filter(Q(title__icontains=search) | Q(content__icontains=search) | Q(user_id=user_id))
            elif search_type == 'title_content':
                boards = Community.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
            elif search_type == 'title':
                boards = Community.objects.filter(title__icontains=search)
            elif search_type == 'content':
                boards = Community.objects.filter(content__icontains=search)
            elif search_type == 'writer':
                user_id = User.objects.get(first_name=search).id
                boards = Community.objects.filter(user_id=user_id)

            if len(boards) == 0:
                boardType = '\'' + str(search) + '\'' + "에 대한 " + "검색 결과가 존재하지 않습니다. "
        except:
            boards = ''
            boardType = "검색 결과가 존재하지 않습니다."
    params = {'boards': boards,
              'boardType': boardType}
    return render(request, 'main/main.html', params)

# 게시판 글쓰는 곳
@login_required(login_url='accounts:login')
def community_write(request):
    data = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')

        grouptype = request.POST.get('grouptype')
        print(grouptype)
        created_date = timezone.now()

        filepath = request.FILES.get('filepath')
        if filepath != None:
            filetype = request.FILES.get('filepath').content_type
        else:
            filepath = ''
            filetype = ''

        data = {'title': title, 'content': content, 'grouptype': grouptype, 'filepath': filepath, 'filetype': filetype}

        if len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')
        elif grouptype == '-':
            messages.warning(request, '게시판 종류를 선택하세요.')
        else:
            try:
                print("check")
                post_add = Community(user_id=request.user, title=title, content=content, type=grouptype,
                                    created_date=created_date, filepath=filepath, filetype=filetype)
                print("ckekf")
                post_add.save()
                return redirect('main:home')
            except:
                messages.warning(request, '게시글 저장에 실패했습니다.')

    return render(request, 'main/write.html', data)

# 게시판 글 읽는
@login_required(login_url='accounts:login')
def community_read(request, communityId):
    currentuser = request.user

    post = get_object_or_404(Community, pk_id=communityId)

    upload_file = str(post.filepath)
    try:
        upload_file = upload_file.split('/')[1]
    except:
        upload_file=''

    comments = Comment.objects.filter(communityid=post.pk_id).order_by('-created_date')

    if comments.count() == 0:
        comments = {}
    params = {'post': post,
              'currentuser': currentuser,
              'comments': comments,
              'upload_file': upload_file}
    return render(request, 'main/read.html', params)

@login_required(login_url='accounts:login')
def community_download(request, communityId):
    post = Community.objects.get(pk_id=communityId)
    file_name = post.filepath.name
    file_path = post.filepath.path
    file_type = post.filetype
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response


@login_required(login_url='accounts:login')
def community_modify(request, communityId):
    post = Community.objects.get(pk_id=communityId)
    data = {'pk_id': post.pk_id, 'title': post.title, 'content': post.content, 'grouptype': post.type,
            'filepath': post.filepath, 'filetype': post.filetype}

    if request.method == 'POST':
        title = request.POST.get('title')
        valid_title = title.replace(' ', '').replace('\n', '')
        post.title = title

        content = request.POST.get('content')
        valid_content = content.replace(' ', '').replace('\n', '')
        post.content = content

        grouptype = request.POST.get('grouptype')
        post.type = grouptype

        filepath = request.FILES.get('filepath')
        if filepath != None:
            post.filepath = filepath
            filetype = request.FILES.get('filepath').content_type
            post.filetype = filetype
        else:
            filepath = post.filepath
            filetype = post.filetype


        data = {'pk_id': post.pk_id, 'title': title, 'content': content, 'grouptype': grouptype,
                'filepath': filepath, 'filetype': filetype}


        if len(valid_title) == 0:
            messages.warning(request, '제목을 입력하세요.')
        elif len(valid_content) == 0:
            messages.warning(request, '내용을 입력하세요.')
        elif grouptype == '-':
            messages.warning(request, '모임 형태를 선택하세요.')
        else:
            post.save()
            return redirect('main:community_read', communityId)

    return render(request, 'main/modify.html', data)


@login_required(login_url='accounts:login')
def community_delete(request, communityId):
    try:
        del_post = Community.objects.get(pk_id=communityId)
        del_post.delete()
    except:
        return redirect('main:home')
    return redirect('main:home')


@login_required(login_url='accounts:login')
def community_comment_write(request, communityId):
    content = request.POST.get('comment')
    created_date = timezone.now()
    post = Community.objects.get(pk_id=communityId)

    valid_content = content.replace(' ', '').replace('\n', '')

    if len(valid_content) != 0:
        comment = Comment.objects.create(communityid=post, content=content, user_id=request.user, created_date=created_date)
        comment.save()
    else:
        messages.warning(request, '공백 댓글은 입력할 수 없습니다.')

    return redirect('main:community_read', communityId)


@login_required(login_url='accounts:login')
def community_comment_delete(request, communityId, commentId):
    try:
        del_comment = Comment.objects.get(pk_id=commentId)
        del_comment.delete()
    except:
        return redirect('main:community_read', communityId)
    return redirect('main:community_read', communityId)

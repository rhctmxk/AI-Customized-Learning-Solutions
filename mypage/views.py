from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from .models import license_select, Video, Alert
import re



@login_required(login_url='accounts:login')
def home(request):
    user = request.user
    user_license = license_select.objects.filter(user_id=user)
    context = {'user_license': user_license}
    return render(request, 'mypage/home.html', context)



@login_required(login_url='accounts:login')
def license(request):
    Data_sum_detail1 = apps.get_model('search', 'Data_sum_detail1')
    Technology_korea = apps.get_model('search', 'Technology_korea')
    Technology_other = apps.get_model('search', 'Technology_other')

    jobs = Data_sum_detail1.objects.all()
    licenses3 = Technology_korea.objects.all()
    licenses4 = Technology_other.objects.all()
    params = {'licenses3': licenses3,
              'licenses4': licenses4,
              'jobs': jobs}

    return render(request, 'mypage/license.html', params)

@login_required(login_url='accounts:login')
def delete_alert(request):
    user = request.user
    alerts = Alert.objects.filter(user=user)

    for alert in alerts:
        alert.activate = 0
        alert.save()


    return redirect('main:home')

# 자격증 찜하는거
@login_required(login_url='accounts:login')
def add_license(request):
    user = request.user
    License_ranking = apps.get_model('search', 'License_raking')
    Technology_korea = apps.get_model('search', 'Technology_korea')
    Technology_other = apps.get_model('search', 'Technology_other')
    if request.method == 'POST':
        license = request.POST['license']
        print("하트눌렀을때")
        print(license)

    try:
        if Technology_korea.objects.filter(license=license, activate=0).exists() or Technology_other.objects.filter(license=license, activate=0).exists():
            print("없는거네")
            return redirect('mypage:license')

        if License_ranking.objects.filter(license=license).exists():
            print("있구나.")
        else:
            license_count = License_ranking.objects.create(license=license, count=1)
            print("생성")
            license_count.save()

        if license_select.objects.filter(user_id=user, license=license).exists():
            user_license = license_select.objects.filter(user_id=user, license=license)
            user_license.delete()
            license_count = License_ranking.objects.get(license=license)
            print(license_count.count)
            license_count.count -= 1
            license_count.save()
            content = '\'' + license + '\' 자격증이 삭제되었습니다.'
            alert_add = Alert.objects.create(content=content, user=user)
            alert_add.save()
        else:
            add = license_select.objects.create(user_id=user, license=license)
            add.save()
            license_count = License_ranking.objects.get(license=license)
            print(license_count.count)
            license_count.count += 1
            license_count.save()
            content = '\'' + license + '\' 자격증이 추가되었습니다.'
            alert_add = Alert.objects.create(content=content, user=user)
            alert_add.save()
            return redirect('mypage:home')
    except:
        print("3")
        return redirect('mypage:home')
    return redirect('mypage:license')

# 스터디, 문제풀이 고르는 곳
@login_required(login_url='accounts:login')
def studylicense(request):
    user = request.user

    return render(request, 'mypage/studylicense.html')

# 동영상 게시판 메인화면
@login_required(login_url='accounts:login')
def theoryVideo(request):
    boards = Video.objects.all()
    boardType = '이론동영상'
    if 'search' in request.POST:
        search = request.POST.get('search')
        boardType = '\'' + str(search) + '\'' + "에 대한 검색 결과 입니다."
        try:
            if re.search('파이썬|데이터베이스|운영체제|디지털|인공지능', search) == None:
                search_process = search.replace(" ", "")  # 조건을 만족하지 못한 검색어를 공백을 지운다.
                processing = re.search('파이썬|데이터베이스|운영체제|디지털|인공지능', search_process)  # 공백을 지운 검색어와 핵심단어를 매칭시켜본다.
                new_search = processing.group()  # 공백을 지운 검색어와 일치하는 핵심단어
                boards = Video.objects.filter(title__icontains=new_search)
                boardType = '\'' + str(new_search) + '\'' + "에 대한 검색 결과 입니다."
                print(new_search)  # 공백을 지운 검색어와 일치하는 핵심단어를 검색하게 한다.
            else:
                boards = Video.objects.filter(title__icontains=search)
                if len(boards) == 0:
                    boardType = '\'' + str(search) + '\'' + "에 대한 " + "검색 결과가 존재하지 않습니다. "
        except:
            boards = ''
            boardType = "검색 결과가 존재하지 않습니다."
    params = {'boards': boards,
              'boardType': boardType}
    return render(request, 'mypage/theoryVideo.html', params)




# 1과목 찜한것
@login_required(login_url='accounts:login')
def my_subject1(request):
    Subject = apps.get_model('note', 'Note')
    Dib_page = apps.get_model('note', 'Page')
    user = request.user
    dib_page = Dib_page.objects.get(user_id=user)
    print(dib_page)
    dib_len = len(Subject.objects.filter(user_id=user, subject=1, dib=1))
    print(dib_len)
    if request.method == 'POST':
        num = Subject.objects.get(page=request.POST['num'], subject=1, dib=1, user_id=user).page
        if 'note' in request.POST:
            if Subject.objects.filter(page=request.POST['num'], dib=1, subject=1, user_id=user).exists():  # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Subject.objects.get(page=request.POST['num'], dib=1, subject=1, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except:  # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Subject.objects.create(note=note, dib=1, page=request.POST['num'], subject=1, user_id=user)
                    user.save()

            else:  # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Subject.objects.create(note=valid_content, dib=1, page=request.POST['num'], subject=1, user_id=user)
                user.save()
        if 'PrePage' in request.POST: # 페이지 넘길때
            dib_page.dib_subject1 = dib_page.dib_subject1 - 1
            if dib_page.dib_subject1 == -1:
                dib_page.dib_subject1 = 0
            dib_page.save()
        if 'PostPage' in request.POST:
            dib_page.dib_subject1 = dib_page.dib_subject1 + 1
            if dib_page.dib_subject1 > dib_len-1:
                dib_page.dib_subject1 = dib_len-1
            dib_page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            num_page = Subject.objects.filter(subject=1, dib=1, user_id=user).order_by('page')
            page = []
            for a in num_page:
                page.append(a.page)
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Subject.objects.get(page=page[dib_page.dib_subject1], subject=1, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()

    user = request.user
    num = Subject.objects.filter(subject=1, dib=1, user_id=user).order_by('page')[0].page
    print(num)
    num_page = Subject.objects.filter(subject=1, dib=1, user_id=user).order_by('page')
    page = []
    for a in num_page:
        page.append(a.page)
    try:
        user_note = Subject.objects.get(page=int(num), subject=1, user_id=user)
        checkeddib = int(Subject.objects.get(page=int(num), subject=1, user_id=user).dib)
    except Subject.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'mypage/note_subject1.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib, 'page': page, 'dib_page': dib_page})


# 2과목 찜한것
@login_required(login_url='accounts:login')
def my_subject2(request):
    Subject = apps.get_model('note', 'Note')
    Dib_page = apps.get_model('note', 'Page')
    user = request.user
    dib_page = Dib_page.objects.get(user_id=user)
    print(dib_page)
    dib_len = len(Subject.objects.filter(user_id=user, subject=2, dib=1))
    print(dib_len)
    if request.method == 'POST':
        num = Subject.objects.get(page=request.POST['num'], subject=2, dib=1, user_id=user).page
        if 'note' in request.POST:
            if Subject.objects.filter(page=request.POST['num'], dib=1, subject=2, user_id=user).exists():  # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Subject.objects.get(page=request.POST['num'], dib=1, subject=2, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except:  # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Subject.objects.create(note=note, dib=1, page=request.POST['num'], subject=2, user_id=user)
                    user.save()

            else:  # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Subject.objects.create(note=valid_content, dib=1, page=request.POST['num'], subject=2, user_id=user)
                user.save()
        if 'PrePage' in request.POST: # 페이지 넘길때
            dib_page.dib_subject2 = dib_page.dib_subject2 - 1
            if dib_page.dib_subject2 == -1:
                dib_page.dib_subject2 = 0
            dib_page.save()
        if 'PostPage' in request.POST:
            dib_page.dib_subject2 = dib_page.dib_subject2 + 1
            if dib_page.dib_subject2 > dib_len-1:
                dib_page.dib_subject2 = dib_len-1
            dib_page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            num_page = Subject.objects.filter(subject=2, dib=1, user_id=user).order_by('page')
            page = []
            for a in num_page:
                page.append(a.page)
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Subject.objects.get(page=page[dib_page.dib_subject1], subject=2, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()

    user = request.user
    num = Subject.objects.filter(subject=2, dib=1, user_id=user).order_by('page')[0].page
    print(num)
    num_page = Subject.objects.filter(subject=2, dib=1, user_id=user).order_by('page')
    page = []
    for a in num_page:
        page.append(a.page)
    try:
        user_note = Subject.objects.get(page=int(num), subject=2, user_id=user)
        checkeddib = int(Subject.objects.get(page=int(num), subject=2, user_id=user).dib)
    except Subject.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'mypage/note_subject2.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib, 'page': page, 'dib_page': dib_page})


# 3과목 찜한것
@login_required(login_url='accounts:login')
def my_subject3(request):
    Subject = apps.get_model('note', 'Note')
    Dib_page = apps.get_model('note', 'Page')
    user = request.user
    dib_page = Dib_page.objects.get(user_id=user)
    print(dib_page)
    dib_len = len(Subject.objects.filter(user_id=user, subject=3, dib=1))
    print(dib_len)
    if request.method == 'POST':
        num = Subject.objects.get(page=request.POST['num'], subject=3, dib=1, user_id=user).page
        if 'note' in request.POST:
            if Subject.objects.filter(page=request.POST['num'], dib=1, subject=3, user_id=user).exists():  # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Subject.objects.get(page=request.POST['num'], dib=1, subject=3, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except:  # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Subject.objects.create(note=note, dib=1, page=request.POST['num'], subject=3, user_id=user)
                    user.save()

            else:  # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Subject.objects.create(note=valid_content, dib=1, page=request.POST['num'], subject=3, user_id=user)
                user.save()
        if 'PrePage' in request.POST: # 페이지 넘길때
            dib_page.dib_subject3 = dib_page.dib_subject3 - 1
            if dib_page.dib_subject3 == -1:
                dib_page.dib_subject3 = 0
            dib_page.save()
        if 'PostPage' in request.POST:
            dib_page.dib_subject3 = dib_page.dib_subject3 + 1
            if dib_page.dib_subject3 > dib_len-1:
                dib_page.dib_subject3 = dib_len-1
            dib_page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            num_page = Subject.objects.filter(subject=3, dib=1, user_id=user).order_by('page')
            page = []
            for a in num_page:
                page.append(a.page)
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Subject.objects.get(page=page[dib_page.dib_subject1], subject=3, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()

    user = request.user
    num = Subject.objects.filter(subject=3, dib=1, user_id=user).order_by('page')[0].page
    print(num)
    num_page = Subject.objects.filter(subject=3, dib=1, user_id=user).order_by('page')
    page = []
    for a in num_page:
        page.append(a.page)
    try:
        user_note = Subject.objects.get(page=int(num), subject=3, user_id=user)
        checkeddib = int(Subject.objects.get(page=int(num), subject=3, user_id=user).dib)
    except Subject.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'mypage/note_subject3.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib, 'page': page, 'dib_page': dib_page})


# 4과목 찜한것
@login_required(login_url='accounts:login')
def my_subject4(request):
    Subject = apps.get_model('note', 'Note')
    Dib_page = apps.get_model('note', 'Page')
    user = request.user
    dib_page = Dib_page.objects.get(user_id=user)
    print(dib_page)
    dib_len = len(Subject.objects.filter(user_id=user, subject=4, dib=1))
    print(dib_len)
    if request.method == 'POST':
        num = Subject.objects.get(page=request.POST['num'], subject=4, dib=1, user_id=user).page
        if 'note' in request.POST:
            if Subject.objects.filter(page=request.POST['num'], dib=1, subject=4, user_id=user).exists():  # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Subject.objects.get(page=request.POST['num'], dib=1, subject=4, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except:  # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Subject.objects.create(note=note, dib=1, page=request.POST['num'], subject=4, user_id=user)
                    user.save()

            else:  # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Subject.objects.create(note=valid_content, dib=1, page=request.POST['num'], subject=4, user_id=user)
                user.save()
        if 'PrePage' in request.POST: # 페이지 넘길때
            dib_page.dib_subject4 = dib_page.dib_subject4 - 1
            if dib_page.dib_subject4 == -1:
                dib_page.dib_subject4 = 0
            dib_page.save()
        if 'PostPage' in request.POST:
            dib_page.dib_subject4 = dib_page.dib_subject4 + 1
            if dib_page.dib_subject4 > dib_len-1:
                dib_page.dib_subject4 = dib_len-1
            dib_page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            num_page = Subject.objects.filter(subject=4, dib=1, user_id=user).order_by('page')
            page = []
            for a in num_page:
                page.append(a.page)
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Subject.objects.get(page=page[dib_page.dib_subject1], subject=4, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()

    user = request.user
    num = Subject.objects.filter(subject=4, dib=1, user_id=user).order_by('page')[0].page
    print(num)
    num_page = Subject.objects.filter(subject=4, dib=1, user_id=user).order_by('page')
    page = []
    for a in num_page:
        page.append(a.page)
    try:
        user_note = Subject.objects.get(page=int(num), subject=4, user_id=user)
        checkeddib = int(Subject.objects.get(page=int(num), subject=4, user_id=user).dib)
    except Subject.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'mypage/note_subject4.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib, 'page': page, 'dib_page': dib_page})


# 5과목 찜한것
@login_required(login_url='accounts:login')
def my_subject5(request):
    Subject = apps.get_model('note', 'Note')
    Dib_page = apps.get_model('note', 'Page')
    user = request.user
    dib_page = Dib_page.objects.get(user_id=user)
    print(dib_page)
    dib_len = len(Subject.objects.filter(user_id=user, subject=5, dib=1))
    print(dib_len)
    if request.method == 'POST':
        num = Subject.objects.get(page=request.POST['num'], subject=5, dib=1, user_id=user).page
        if 'note' in request.POST:
            if Subject.objects.filter(page=request.POST['num'], dib=1, subject=5, user_id=user).exists():  # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Subject.objects.get(page=request.POST['num'], dib=1, subject=5, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except:  # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Subject.objects.create(note=note, dib=1, page=request.POST['num'], subject=5, user_id=user)
                    user.save()

            else:  # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Subject.objects.create(note=valid_content, dib=1, page=request.POST['num'], subject=5, user_id=user)
                user.save()
        if 'PrePage' in request.POST: # 페이지 넘길때
            dib_page.dib_subject5 = dib_page.dib_subject5 - 1
            if dib_page.dib_subject5 == -1:
                dib_page.dib_subject5 = 0
            dib_page.save()
        if 'PostPage' in request.POST:
            dib_page.dib_subject5 = dib_page.dib_subject5 + 1
            if dib_page.dib_subject5 > dib_len-1:
                dib_page.dib_subject5 = dib_len-1
            dib_page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            num_page = Subject.objects.filter(subject=5, dib=1, user_id=user).order_by('page')
            page = []
            for a in num_page:
                page.append(a.page)
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Subject.objects.get(page=page[dib_page.dib_subject1], subject=5, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()

    user = request.user
    num = Subject.objects.filter(subject=5, dib=1, user_id=user).order_by('page')[0].page
    print(num)
    num_page = Subject.objects.filter(subject=5, dib=1, user_id=user).order_by('page')
    page = []
    for a in num_page:
        page.append(a.page)
    try:
        user_note = Subject.objects.get(page=int(num), subject=5, user_id=user)
        checkeddib = int(Subject.objects.get(page=int(num), subject=5, user_id=user).dib)
    except Subject.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'mypage/note_subject5.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib, 'page': page, 'dib_page': dib_page})
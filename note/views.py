from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Note
from .models import Page


# Create your views here.
@login_required(login_url='accounts:login')
def note_main(request):
    return render(request, 'note/main.html')

@login_required(login_url='accounts:login')
def select_subject(request):
    user = request.user
    subject_1 = Note.objects.filter(user_id=user, dib=1, subject=1)
    subject_2 = Note.objects.filter(user_id=user, dib=1, subject=2)
    subject_3 = Note.objects.filter(user_id=user, dib=1, subject=3)
    subject_4 = Note.objects.filter(user_id=user, dib=1, subject=4)
    subject_5 = Note.objects.filter(user_id=user, dib=1, subject=5)
    params = {'subject_1': subject_1,
              'subject_2': subject_2,
              'subject_3': subject_3,
              'subject_4': subject_4,
              'subject_5': subject_5}
    return render(request, 'note/select_subject.html', params)

@login_required(login_url='accounts:login')
def note_subject1(request):
    user = request.user
    try:
        num = Page.objects.get(user_id=user).page_subject1  # 해당 사용자에 맞는 페이지 가져옴.
    except: # 사용자의 페이지가 없다면 새로 생성
        user_page = Page.objects.create(page_subject1=1, page_subject2=1, page_subject3=1, page_subject4=1, page_subject5=1, user_id=user)
        user_page.save()
        num = Page.objects.get(user_id=user).page_subject1  # 해당 사용자에 맞는 페이지 가져옴.
    if request.method == 'POST':
        page = Page.objects.get(user_id=user)
        if 'note' in request.POST:
            if Note.objects.filter(page=request.POST['num'], subject=1, user_id=user).exists(): # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Note.objects.get(page=request.POST['num'], subject=1, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except: # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Note.objects.create(note=note, page=request.POST['num'], subject=1, user_id=user)
                    user.save()

            else: # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Note.objects.create(note=valid_content, page=request.POST['num'], subject=1, user_id=user)
                user.save()

        if 'PrePage' in request.POST: # 페이지 넘길때
            page.page_subject1 = int(request.POST['PrePage'])
            page.save()
        if 'PostPage' in request.POST:
            page.page_subject1 = int(request.POST['PostPage'])
            page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Note.objects.get(page=int(num), subject=1, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()

    user = request.user
    num = Page.objects.get(user_id=user).page_subject1

    try:
        user_note = Note.objects.get(page=int(num), subject=1, user_id=user)
        checkeddib = int(Note.objects.get(page=int(num), subject=1, user_id=user).dib)
    except Note.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'note/note_subject1.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib})

@login_required(login_url='accounts:login')
def note_subject2(request):
    user = request.user
    try:
        num = Page.objects.get(user_id=user).page_subject2  # 해당 사용자에 맞는 페이지 가져옴.
    except: # 사용자의 페이지가 없다면 새로 생성
        user_page = Page.objects.create(page_subject1=1, page_subject2=1, page_subject3=1, page_subject4=1, page_subject5=1, user_id=user)
        user_page.save()
        num = Page.objects.get(user_id=user).page_subject2  # 해당 사용자에 맞는 페이지 가져옴.
    if request.method == 'POST':
        page = Page.objects.get(user_id=user)
        if 'note' in request.POST:
            if Note.objects.filter(page=request.POST['num'], subject=2, user_id=user).exists(): # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Note.objects.get(page=request.POST['num'], subject=2, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except: # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Note.objects.create(note=note, page=request.POST['num'], subject=2, user_id=user)
                    user.save()

            else: # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Note.objects.create(note=valid_content, page=request.POST['num'], subject=2, user_id=user)
                user.save()

        if 'PrePage' in request.POST: # 페이지 넘길때
            page.page_subject2 = int(request.POST['PrePage'])
            page.save()
        if 'PostPage' in request.POST:
            page.page_subject2 = int(request.POST['PostPage'])
            page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Note.objects.get(page=int(num), subject=2, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()
    user = request.user
    num = Page.objects.get(user_id=user).page_subject2
    try:
        user_note = Note.objects.get(page=int(num), subject=2, user_id=user)
        checkeddib = int(Note.objects.get(page=int(num), subject=2, user_id=user).dib)
    except Note.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'note/note_subject2.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib})

@login_required(login_url='accounts:login')
def note_subject3(request):
    user = request.user
    try:
        num = Page.objects.get(user_id=user).page_subject3  # 해당 사용자에 맞는 페이지 가져옴.
    except: # 사용자의 페이지가 없다면 새로 생성
        user_page = Page.objects.create(page_subject1=1, page_subject2=1, page_subject3=1, page_subject4=1, page_subject5=1, user_id=user)
        user_page.save()
        num = Page.objects.get(user_id=user).page_subject3  # 해당 사용자에 맞는 페이지 가져옴.
    if request.method == 'POST':
        page = Page.objects.get(user_id=user)
        if 'note' in request.POST:
            if Note.objects.filter(page=request.POST['num'], subject=3, user_id=user).exists(): # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Note.objects.get(page=request.POST['num'], subject=3, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except: # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Note.objects.create(note=note, page=request.POST['num'], subject=3, user_id=user)
                    user.save()

            else: # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Note.objects.create(note=valid_content, page=request.POST['num'], subject=3, user_id=user)
                user.save()

        if 'PrePage' in request.POST: # 페이지 넘길때
            page.page_subject3 = int(request.POST['PrePage'])
            page.save()
        if 'PostPage' in request.POST:
            page.page_subject3 = int(request.POST['PostPage'])
            page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Note.objects.get(page=int(num), subject=3, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()
    user = request.user
    num = Page.objects.get(user_id=user).page_subject3
    try:
        user_note = Note.objects.get(page=int(num), subject=3, user_id=user)
        checkeddib = int(Note.objects.get(page=int(num), subject=3, user_id=user).dib)
    except Note.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'note/note_subject3.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib})

@login_required(login_url='accounts:login')
def note_subject4(request):
    user = request.user
    try:
        num = Page.objects.get(user_id=user).page_subject4  # 해당 사용자에 맞는 페이지 가져옴.
    except: # 사용자의 페이지가 없다면 새로 생성
        user_page = Page.objects.create(page_subject1=1, page_subject2=1, page_subject3=1, page_subject4=1, page_subject5=1, user_id=user)
        user_page.save()
        num = Page.objects.get(user_id=user).page_subject4  # 해당 사용자에 맞는 페이지 가져옴.
    if request.method == 'POST':
        page = Page.objects.get(user_id=user)
        if 'note' in request.POST:
            if Note.objects.filter(page=request.POST['num'], subject=4, user_id=user).exists(): # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Note.objects.get(page=request.POST['num'], subject=4, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except: # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Note.objects.create(note=note, page=request.POST['num'], subject=4, user_id=user)
                    user.save()

            else: # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Note.objects.create(note=valid_content, page=request.POST['num'], subject=4, user_id=user)
                user.save()

        if 'PrePage' in request.POST: # 페이지 넘길때
            page.page_subject4 = int(request.POST['PrePage'])
            page.save()
        if 'PostPage' in request.POST:
            page.page_subject4 = int(request.POST['PostPage'])
            page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Note.objects.get(page=int(num), subject=4, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()
    user = request.user
    num = Page.objects.get(user_id=user).page_subject4
    try:
        user_note = Note.objects.get(page=int(num), subject=4, user_id=user)
        checkeddib = int(Note.objects.get(page=int(num), subject=4, user_id=user).dib)
    except Note.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'note/note_subject4.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib})

@login_required(login_url='accounts:login')
def note_subject5(request):
    user = request.user
    try:
        num = Page.objects.get(user_id=user).page_subject5  # 해당 사용자에 맞는 페이지 가져옴.
    except: # 사용자의 페이지가 없다면 새로 생성
        user_page = Page.objects.create(page_subject1=1, page_subject2=1, page_subject3=1, page_subject4=1, page_subject5=1, user_id=user)
        user_page.save()
        num = Page.objects.get(user_id=user).page_subject5  # 해당 사용자에 맞는 페이지 가져옴.
    if request.method == 'POST':
        page = Page.objects.get(user_id=user)
        if 'note' in request.POST:
            if Note.objects.filter(page=request.POST['num'], subject=5, user_id=user).exists(): # 해당 페이지에 노트된곳이 있을때,
                try:
                    pre_note = Note.objects.get(page=request.POST['num'], subject=5, user_id=user)
                    pre_note.note = request.POST['note']
                    pre_note.save()
                except: # 해당 페이지에 노트된곳이 없을때
                    note = request.POST['note']
                    user = Note.objects.create(note=note, page=request.POST['num'], subject=5, user_id=user)
                    user.save()

            else: # 해당페이지에 노트된게 없을때
                note = request.POST['note']
                valid_content = note.replace(' ', '').replace('\n', '')
                user = Note.objects.create(note=valid_content, page=request.POST['num'], subject=5, user_id=user)
                user.save()

        if 'PrePage' in request.POST: # 페이지 넘길때
            page.page_subject5 = int(request.POST['PrePage'])
            page.save()
        if 'PostPage' in request.POST:
            page.page_subject5 = int(request.POST['PostPage'])
            page.save()
        if 'checkeddib' in request.POST:
            user = request.user
            dib = int(request.POST['checkeddib'])
            if dib == 0:
                dib = 1
            elif dib == 1:
                dib = 0
            checkeddib = Note.objects.get(page=int(num), subject=5, user_id=user)
            checkeddib.dib = dib
            checkeddib.save()
    user = request.user
    num = Page.objects.get(user_id=user).page_subject5
    try:
        user_note = Note.objects.get(page=int(num), subject=5, user_id=user)
        checkeddib = int(Note.objects.get(page=int(num), subject=5, user_id=user).dib)
    except Note.DoesNotExist:
        user_note = None
        checkeddib = None
    return render(request, 'note/note_subject5.html', {'num': num, 'user_note': user_note, 'checkeddib': checkeddib})
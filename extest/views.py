from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import PREVIOUS_EXERCISE_SUMMARY
from .models import PREVIOUS_EXERCISE_EXAM
from .models import PREVIOUS_EXERCISE_FIGURE_TABLE
from .models import PREVIOUS_EXERCISE_QUES
from .models import PREVIOUS_EXERCISE_EXAM_ANSWER
from .models import PREVIOUS_EXERCISE_EXAM_RESULT
from django.apps import apps
from django.db.models import Max
import requests
import re
from django.db.models import Q
gdivision = 1

@login_required(login_url='accounts:login')
def studymain(request):
    return render(request, 'extest/studymain.html')

@login_required(login_url='accounts:login')
def test(request):
    return render(request, 'extest/test.html')

@login_required(login_url='accounts:login')
def omrstart(request) :
    return render(request, 'extest/omrstart.html')

# Create your views here.
@login_required(login_url='accounts:login')
def omrtest(request):
    # DB_que = PREVIOUS_EXERCISE_QUES.objects.all().order_by("?")[0:30:1]

    user = request.user
    global gdivision
    if request.method == 'POST':

        que_id = []
        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        division = 0
        num_count = 1

        count = request.POST['count']
        select_value = request.POST['select_value']

        DB_que = None
        subject = request.POST.getlist('subject')
        subject = list(map(int, subject))

        print(subject)

        print(select_value)
        if select_value == '상' or select_value == '중' or select_value == '하':
            for i in subject:
                if (DB_que == None):
                    DB_que = PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i, PRE_EXE_QUES_DIFFICULTY=select_value).order_by("?")[0:int(count, 10):1]
                else:
                    DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i, PRE_EXE_QUES_DIFFICULTY=select_value).order_by("?")[0:int(count, 10):1]
        elif select_value == '랜덤' :
            for i in subject:
                if (DB_que == None):
                    DB_que = PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i).order_by("?")[0:int(count, 10):1]
                else:
                    DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i).order_by("?")[0:int(count, 10):1]

        # DB_que = PREVIOUS_EXERCISE_QUES.objects.all().order_by()[0:int(count, 10):1]

        obj = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.last()
        print(obj)
        if(obj == None) :
            division = 1
            print(division)
        else :
            division = obj.DIVISION + 1

        for i in DB_que:
            que_id.append(i.PK_ID)
            questions.append(i.PRE_EXE_QUES_QUESTION)
            que_FK.append(i.PK_ID)
            str3 = str(i.ANSWER)
            # str3 = str3.split()
            str3 = re.split('[(|)| ]', str3)
            print(str3[3])
            answer = PREVIOUS_EXERCISE_EXAM.objects.filter(PK_ID=str3[3])

            for j in answer:
                answer2 = j.PRE_EXAM_NUM

            PREVIOUS_EXERCISE_EXAM_ANSWER.objects.create(
                SELECT=3,
                DIVISION=division,
                QUE_NUM=num_count,
                QUE_ID=i.PK_ID,
                USER_ID=user,
                ANSWER_NUM=answer2,
                ANSWER_CHECK=0
            )
            num_count += 1

        print("division = "+ str(division))
        gdivision = division

        for i in que_FK :
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content :
                if j.PRE_EXAM_NUM == 1 :
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2 :
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3 :
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4 :
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        # User.objects.create_user(
        #     first_name=first_name,
        #     username=username,
        #     password=password1,
        #     birth_date=birth_date,
        #     email=email,
        #     location=location,
        #     mobile=c1
        # )

        problem_list =[]
        problem = []

        for i in range(1, num_count):
            count_list.append(i)

        for i, j, k in zip(questions, item_contents, count_list):
            problem = [i]+j+[k]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        print(count_list)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/omrtest.html', {'page_obj': page_obj, 'count':count_list, 'division':division})

    if request.method == 'GET' :
        # que_select = request.POST['hidden_text[]']
        # print(que_select)
        # division = request.GET['division']
        # print(division)

        # DB_que = PREVIOUS_EXERCISE_QUES.objects.all().order_by()[0:int(count, 10):1]

        print(gdivision)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        count = 0

        for i in DB_que:
            question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            for j in question:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)
            # questions.append(i.PRE_EXE_QUES_QUESTION)
            count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        answer_que_list = []
        for i in answer_que :
            answer_que_list.append(i.ANSWER_CHECK)

        problem_list = []
        problem = []

        for i in range(1, int(count)+1):
            count_list.append(i)

        for i, j, k, z in zip(questions, item_contents, count_list, answer_que_list):
            problem = [i] + j + [k] + [z]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/omrtest.html', {'page_obj': page_obj, 'count':count_list, 'answer_que': answer_que_list})

def nonlogin_abilitystart(request):
    TECHNOLOGY_KOREA = apps.get_model('search', 'Technology_korea')

    DB_QUE = TECHNOLOGY_KOREA.objects.all().order_by('license')

    return render(request, 'extest/nonlogin_abilitystart.html', {'DB_QUE' : DB_QUE})

@login_required(login_url='accounts:login')
def wrongview(request) :

    user = request.user


    boards = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(USER_ID=user).order_by('-DIVISION')
    board_type = ''

    if request.method == 'POST':
        board_type = request.POST.get('board_type')

    try:
        if board_type == 'boards':
                boards = PREVIOUS_EXERCISE_EXAM_RESULT.objects.all().order_by('-DIVISION')
        elif board_type == 'ability':
                boards = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(SELECT=1, USER_ID=user).order_by('-DIVISION')
        elif board_type == 'previous':
                boards = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(SELECT=2, USER_ID=user).order_by('-DIVISION')
        elif board_type == 'free':
                boards = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(SELECT=3, USER_ID=user).order_by('-DIVISION')

    except:
        print("error")

        ability = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(SELECT=1, USER_ID=user).order_by('-DIVISION')
        previous = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(SELECT=2, USER_ID=user).order_by('-DIVISION')
        level = PREVIOUS_EXERCISE_EXAM_RESULT.objects.filter(SELECT=3, USER_ID=user).order_by('-DIVISION')

    print(boards)
    # params = {'boards': boards}
    return render(request, 'extest/wrongview.html', {'boards': boards})



@login_required(login_url='accounts:login')
def wrongstart(request) :
    user = request.user

    division = request.POST['division']

    return render(request, 'extest/wrongstart.html', {'division':division})

@login_required(login_url='accounts:login')
def wrongtest(request) :
    user = request.user
    global gdivision

    if 'gettext' in request.POST:
        # text = str(request.POST.get('gettext'))  # 문제 지문 받아오기
        # print(text)
        # url_items = "http://192.168.219.101:5000/add"
        # data = text
        #
        # response = requests.post(url_items, json=data)
        # print(response.text)
        return redirect('reco:compare')

    if request.method == 'POST':
        select_value = request.POST['select_value']
        print(select_value)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=select_value)

        que_id = []
        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        division = 0
        num_count = 1
        count = 0

        obj = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.last()
        print(obj)
        if (obj == None):
            division = 1
            print(division)
        else:
            division = obj.DIVISION + 1

        for i in DB_que:
            if i.ANSWER_NUM != i.ANSWER_CHECK:
                que_id.append(i.QUE_ID)
                count += 1


        for i in que_id:
            DB_que2 = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i)

            for j in DB_que2:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)

                PREVIOUS_EXERCISE_EXAM_ANSWER.objects.create(
                    SELECT=4,
                    DIVISION=division,
                    QUE_NUM=num_count,
                    QUE_ID=i,
                    USER_ID=user,
                    ANSWER_NUM=4,
                    ANSWER_CHECK=0
                )
                num_count += 1

        print("division = " + str(division))
        gdivision = division

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        problem_list = []
        problem = []

        for i in range(1, num_count):
            count_list.append(i)

        for i, j, k in zip(questions, item_contents, count_list):
            problem = [i] + j + [k]
            problem_list.append(problem)

        print(count_list)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        return render(request, 'extest/wrongtest.html',
                      {'page_obj': page_obj, 'count': count_list, 'division': division})

    if request.method == 'GET':

        print(gdivision)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        count = 0

        for i in DB_que:
            question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            for j in question:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)
            # questions.append(i.PRE_EXE_QUES_QUESTION)
            count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        answer_que_list = []
        for i in answer_que:
            answer_que_list.append(i.ANSWER_CHECK)

        problem_list = []
        problem = []

        for i in range(1, count):
            count_list.append(i)

        for i, j, k, z in zip(questions, item_contents, count_list, answer_que_list):
            problem = [i] + j + [k] + [z]
            problem_list.append(problem)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        return render(request, 'extest/wrongtest.html',
                      {'page_obj': page_obj, 'count': count_list, 'answer_que': answer_que_list})
    return render(request, 'extest/wrongtest.html')

@login_required(login_url='accounts:login')
def wrongreview(request) :
    global gdivision
    if request.method == 'POST':
        select_value = request.POST['select_value']

        print(select_value)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=select_value)

        que_id = []
        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        division = 0
        num_count = 1
        answer_que_list = []
        collect_que_answer = []

        for i in DB_que:
            que = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            que_id.append(i.QUE_ID)
            answer_que_list.append(i.ANSWER_CHECK)
            collect_que_answer.append(i.ANSWER_NUM)

            for j in que:
                questions.append(j.PRE_EXE_QUES_QUESTION)
            que_FK.append(i.QUE_ID)

            num_count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        problem_list = []
        problem = []

        for i in range(1, num_count):
            count_list.append(i)

        for i, j, k, z, y in zip(questions, item_contents, count_list, answer_que_list, collect_que_answer):
            problem = [i] + j + [k] + [z] + [y]
            problem_list.append(problem)

        print(count_list)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        return render(request, 'extest/result_omr.html',
                      {'page_obj': page_obj, 'count': count_list, 'division': division, 'answer_que': answer_que_list})

    if request.method == 'GET':
        print(gdivision)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        count = 0

        answer_que_list = []
        collect_que_answer = []

        for i in DB_que:
            question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            answer_que_list.append(i.ANSWER_CHECK)
            collect_que_answer.append(i.ANSWER_NUM)

            for j in question:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)
            # questions.append(i.PRE_EXE_QUES_QUESTION)
            count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        for i in answer_que:
            answer_que_list.append(i.ANSWER_CHECK)

        problem_list = []
        problem = []

        for i in range(1, count):
            count_list.append(i)

        for i, j, k, z, y in zip(questions, item_contents, count_list, answer_que_list, collect_que_answer):
            problem = [i] + j + [k] + [z] + [y]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/result_omr.html',
                      {'page_obj': page_obj, 'count': count_list, 'answer_que': answer_que_list})


@login_required(login_url='accounts:login')
def cancle_omr(request) :
    global gdivision

    PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision).delete()

    return redirect('main:home')
    # return redirect(request, 'mypage/')

@login_required(login_url='accounts:login')
def submit_omr(request) :
    global gdivision
    count = 0
    que_count = 0

    ans_check = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision).all()

    for i in ans_check:
        if i.ANSWER_NUM == i.ANSWER_CHECK :
            count += 1
        que_count += 1

    PREVIOUS_EXERCISE_EXAM_RESULT.objects.create(
        DIVISION=gdivision,
        QUE_COUNT=que_count,
        ANSWER_COUNT=count
    )

    return render(request, 'extest/submit_study.html', {'count' : count, 'que_count' : que_count})



@login_required(login_url='accounts:login')
def data_save(request):
        global gdivision
        print(gdivision)
        id = request.GET.get('id', False)
        value = request.GET.get('value',False)
        # que_select = request.GET['que_select']
        print(id)
        print(value)

        print(PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(QUE_NUM=id, DIVISION=gdivision))

        PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(QUE_NUM=id, DIVISION=gdivision).update(ANSWER_CHECK=value)

        # item = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.get(QUE_ID=id)
        # item.ANSWER_CHECK = value
        # item.save()
        print("입력")

        eng = "성공"
        context= {'eng':eng}

        return JsonResponse(context)


def abilitystart(request):
    return render(request, 'extest/abilitystart.html')


def abilitytest(request) :
    global gdivision
    if request.method == 'POST':

        DB_que=None
        subject = request.POST.getlist('subject')
        subject = list(map(int, subject))
        if len(subject) == 0:
            subject = [1,2,3,4,5]
        print(len(subject))
        user = request.user

        # DB_que = PREVIOUS_EXERCISE_QUES.objects.filter(PRE_EXE_QUES_DIFFICULTY="상상")

        print(DB_que)

        for i in subject:
            print(i)

        for i in subject:
            if(DB_que == None):
                DB_que = PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i,
                                                                PRE_EXE_QUES_DIFFICULTY="상").order_by("?")[0:2:1]
                DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i,
                                                                PRE_EXE_QUES_DIFFICULTY="중").order_by("?")[0:2:1]
                DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i,
                                                                PRE_EXE_QUES_DIFFICULTY="하").order_by("?")[0:2:1]
            else:
                DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i,
                                                               PRE_EXE_QUES_DIFFICULTY="상").order_by("?")[0:2:1]
                DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i,
                                                                PRE_EXE_QUES_DIFFICULTY="중").order_by("?")[0:2:1]
                DB_que += PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=i,
                                                                PRE_EXE_QUES_DIFFICULTY="하").order_by("?")[0:2:1]

        print(len(DB_que))

        que_id = []
        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        division = 0
        num_count = 1

        obj = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.last()
        print(obj)
        if (obj == None):
            division = 1
        else:
            division = obj.DIVISION + 1

        for i in DB_que:
            que_id.append(i.PK_ID)
            questions.append(i.PRE_EXE_QUES_QUESTION)
            que_FK.append(i.PK_ID)

            str3 = str(i.ANSWER)
            # str3 = str3.split()
            str3 = re.split('[(|)| ]', str3)
            answer = PREVIOUS_EXERCISE_EXAM.objects.filter(PK_ID=str3[3])

            for j in answer:
                answer2 = j.PRE_EXAM_NUM

            PREVIOUS_EXERCISE_EXAM_ANSWER.objects.create(
                SELECT=1,
                DIVISION=division,
                QUE_NUM=num_count,
                QUE_ID=i.PK_ID,
                USER_ID=user,
                ANSWER_NUM=answer2,
                ANSWER_CHECK=0
            )
            num_count += 1

        print("division = " + str(division))
        gdivision = division

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        # User.objects.create_user(
        #     first_name=first_name,
        #     username=username,
        #     password=password1,
        #     birth_date=birth_date,
        #     email=email,
        #     location=location,
        #     mobile=c1
        # )

        problem_list = []
        problem = []

        for i in range(1, num_count):
            count_list.append(i)

        for i, j, k in zip(questions, item_contents, count_list):
            problem = [i] + j + [k]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        print(count_list)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/omrtest.html', {'page_obj': page_obj, 'count': count_list, 'division': division})

    if request.method == 'GET':
        # que_select = request.POST['hidden_text[]']
        # print(que_select)
        # division = request.GET['division']
        # print(division)

        # DB_que = PREVIOUS_EXERCISE_QUES.objects.all().order_by()[0:int(count, 10):1]

        print(gdivision)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        count = 0

        for i in DB_que:
            question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            for j in question:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)
            # questions.append(i.PRE_EXE_QUES_QUESTION)
            count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        answer_que_list = []
        for i in answer_que:
            answer_que_list.append(i.ANSWER_CHECK)

        problem_list = []
        problem = []

        for i in range(1, count):
            count_list.append(i)

        for i, j, k, z in zip(questions, item_contents, count_list, answer_que_list):
            problem = [i] + j + [k] + [z]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/omrtest.html',{'page_obj': page_obj, 'count': count_list, 'answer_que': answer_que_list})

@login_required(login_url='accounts:login')
def previousstart(request) :
    user = request.user

    division = []
    year = []

    DB_que = PREVIOUS_EXERCISE_SUMMARY.objects.filter(PRE_EXE_CLASS=1).distinct().values_list('PRE_EXE_YEAR')
    for i in DB_que:
        year.append(i[0])

    year.sort(reverse=True)
    print(year)

    return render(request, 'extest/previousstart.html', {'year': year})


@login_required(login_url='accounts:login')
def previoustest(request) :
    global gdivision
    if request.method == 'POST':

        user = request.user

        select_value = request.POST['select_value']
        select_value2 = request.POST['select_value2']

        select = PREVIOUS_EXERCISE_SUMMARY.objects.filter(PRE_EXE_YEAR=select_value, PRE_EXE_NUMBER=select_value2).all()

        summary = select[0].PK_ID

        DB_que = PREVIOUS_EXERCISE_QUES.objects.filter(FK_PREVIOUS_EXERCISE_SUMMARY=summary).all()

        # DB_que = PREVIOUS_EXERCISE_QUES.objects.all().order_by()[0:int(count, 10):1]

        que_id = []
        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        division = 0
        num_count = 1
        answer = 0

        obj = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.last()
        if (obj == None):
            division = 1
            print(division)
        else:
            division = obj.DIVISION + 1

        for i in DB_que:
            que_id.append(i.PK_ID)
            questions.append(i.PRE_EXE_QUES_QUESTION)
            que_FK.append(i.PK_ID)

            str3 = str(i.ANSWER)
            # str3 = str3.split()
            str3 = re.split('[(|)| ]', str3)
            print(str3[3])
            answer = PREVIOUS_EXERCISE_EXAM.objects.filter(PK_ID=str3[3])

            for j in answer:
                answer2 = j.PRE_EXAM_NUM


            PREVIOUS_EXERCISE_EXAM_ANSWER.objects.create(
                SELECT=2,
                DIVISION=division,
                QUE_NUM=num_count,
                QUE_ID=i.PK_ID,
                USER_ID=user,
                ANSWER_NUM=answer2,
                ANSWER_CHECK=0
            )
            num_count += 1

        print("division = " + str(division))
        gdivision = division

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        problem_list = []
        problem = []

        for i in range(1, num_count):
            count_list.append(i)

        for i, j, k in zip(questions, item_contents, count_list):
            problem = [i] + j + [k]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        print(count_list)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/omrtest.html', {'page_obj': page_obj, 'count': count_list, 'division': division})

    if request.method == 'GET':
        # que_select = request.POST['hidden_text[]']
        # print(que_select)
        # division = request.GET['division']
        # print(division)

        # DB_que = PREVIOUS_EXERCISE_QUES.objects.all().order_by()[0:int(count, 10):1]

        user = request.user
        user_dv = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(USER_ID=user)
        user_dv = user_dv.aggregate(Max('DIVISION'))

        print(gdivision)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(USER_ID=user, DIVISION=user_dv['DIVISION__max'])

        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        count = 1

        for i in DB_que:
            question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            for j in question:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)
            # questions.append(i.PRE_EXE_QUES_QUESTION)
            count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        answer_que_list = []
        for i in answer_que:
            answer_que_list.append(i.ANSWER_CHECK)

        problem_list = []
        problem = []

        for i in range(1, count):
            count_list.append(i)

        for i, j, k, z in zip(questions, item_contents, count_list, answer_que_list):
            problem = [i] + j + [k] + [z]
            problem_list.append(problem)


        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        return render(request, 'extest/omrtest.html',
                      {'page_obj': page_obj, 'count': count_list, 'answer_que': answer_que_list})

@login_required(login_url='accounts:login')
def result_omr(request) :
    global gdivision
    if request.method == 'POST':
        user = request.user
        obj = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.last()
        select_value = obj.DIVISION

        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=select_value)

        que_id = []
        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        division = 0
        num_count = 1
        collect_num_count = 0
        answer_que_list = []
        collect_que_answer = []
        select = 0


        for i in DB_que:
            select = i.SELECT
            que = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            que_id.append(i.QUE_ID)
            answer_que_list.append(i.ANSWER_CHECK)
            collect_que_answer.append(i.ANSWER_NUM)

            if i.ANSWER_CHECK == i.ANSWER_NUM :
                collect_num_count += 1
            for j in que :
                questions.append(j.PRE_EXE_QUES_QUESTION)
            que_FK.append(i.QUE_ID)

            num_count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]


        problem_list = []
        problem = []

        PREVIOUS_EXERCISE_EXAM_RESULT.objects.create(
            SELECT=select,
            DIVISION=select_value,
            QUE_COUNT=num_count-1,
            ANSWER_COUNT=collect_num_count,
            USER_ID=user,
        )


        for i in range(1, num_count):
            count_list.append(i)

        for i, j, k, z ,y in zip(questions, item_contents, count_list, answer_que_list, collect_que_answer):
            problem = [i] + j + [k] + [z] + [y]
            problem_list.append(problem)

        print(count_list)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        return render(request, 'extest/result_omr.html', {'page_obj': page_obj, 'count': count_list, 'division': division, 'answer_que': answer_que_list})

    if request.method == 'GET':
        print(gdivision)
        DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        questions = []
        que_FK = []
        item1 = []
        item2 = []
        item3 = []
        item4 = []
        item_contents = []
        count_list = []
        count = 0

        answer_que_list = []
        collect_que_answer = []

        for i in DB_que:
            question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
            answer_que_list.append(i.ANSWER_CHECK)
            collect_que_answer.append(i.ANSWER_NUM)

            for j in question:
                questions.append(j.PRE_EXE_QUES_QUESTION)
                que_FK.append(j.PK_ID)
            # questions.append(i.PRE_EXE_QUES_QUESTION)
            count += 1

        for i in que_FK:
            item1 = []
            content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
            for j in content:
                if j.PRE_EXAM_NUM == 1:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 2:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 3:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
                elif j.PRE_EXAM_NUM == 4:
                    item1.append(j.PRE_EXAM_SUBSTANCE)
            item_contents += [item1]

        answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)

        for i in answer_que:
            answer_que_list.append(i.ANSWER_CHECK)

        problem_list = []
        problem = []

        for i in range(1, 31):
            count_list.append(i)

        for i, j, k, z, y in zip(questions, item_contents, count_list, answer_que_list,collect_que_answer):
            problem = [i] + j + [k] + [z] + [y]
            problem_list.append(problem)

        # print(problem_list)

        # page = request.GET.get('page', '1')
        # paginator = Paginator(DB_que, '6')
        # page_obj = paginator.get_page(page)

        page = request.GET.get('page', '1')
        paginator = Paginator(problem_list, '6')
        page_obj = paginator.get_page(page)

        # context = {'question_list' : page_obj}

        # return render(request, 'omrtest.html', context)
        return render(request, 'extest/result_omr.html', {'page_obj': page_obj, 'count': count_list, 'answer_que': answer_que_list})
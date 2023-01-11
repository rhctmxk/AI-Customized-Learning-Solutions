from django.contrib.auth.decorators import login_required

from .models import SimilarFileUpload
from .models import DeepExercise
# OCR 라이브러리들
import json
import base64
import requests
import re # 전처리 할려고
from django.shortcuts import render, redirect
import requests


# 모르는 문제 올리는 곳
@login_required(login_url='accounts:login')
def similar_problem(request) :
    user = request.user
    if request.method == 'POST':
        route = "./media/" # media 경로에 넣기 위해서
        global count
        count = int(request.POST['count'])
        # # 이미지 업로드 안했을때
        # if not request.FILES["imgfile"] :
        #     print('abcd')
        #     return render(request, 'site.html', {'error': '오답문제 없을때'})

        img = request.FILES["imgfile"] # 이미지 파일
        a = str(img) # 이미지 파일이름 DB에 저장하기 위해서 문자열로 바꿈
        b = a.split('.') # 원래 이미지파일이 .png의 확장자를 가져서 txt도 하나 만들기 위해서 나눔
        name = b[0] + '.txt' # 위에서 나눈거랑 txt합쳐서 OCR로 추출된것을 이미지파일.txt에 저장

        fileupload = SimilarFileUpload( # DB에 저장
            imgfile=img, # 이게 media에 사진이 저장이 됌.
            image_route=route+name,
            user_id=user
        )

        fileupload.save()

        global c
        c = route + name # OCR로 추출된 txt 파일
        with open(route + str(img), "rb") as f: # 파일을 읽어서 전처리 할꺼임.
            img = base64.b64encode(f.read())

        # 본인의 APIGW Invoke URL로 치환
        URL = "https://25b6c1f481684138938225b6ebe4de50.apigw.ntruss.com/custom/v1/9958/828526be5f74aec7d2496ca173838c9b074940505f800beb0e73bf841d1fa0f9/general"

        # 본인의 Secret Key로 치환
        KEY = "aUR4Ukl6RnlNV1lwa29YU0RwYlZMWHVqcXh6UFZwSEk="

        headers = {
            "Content-Type": "application/json",
            "X-OCR-SECRET": KEY
        }

        data = {
            "version": "V1",
            "requestId": "sample_id",  # 요청을 구분하기 위한 ID, 사용자가 정의
            "timestamp": 0,  # 현재 시간값
            "images": [
                {
                    "name": "sample_image",
                    "format": "png",
                    "data": img.decode('utf-8')
                }
            ]
        }
        data = json.dumps(data)
        response = requests.post(URL, data=data, headers=headers)
        res = json.loads(response.text)
        data1 = []


        with open(route + name, "w") as stdout:
            while True:
                try:
                    for i in range(100):
                        data2 = (res['images'][0]['fields'][i]['inferText'])
                        print("데이터 2 어떻게 나올까?")
                        print(data2) # data2는 .split(" ")의 느낌으로 띄어쓰기로 기준으로 한단어 씩 추출한다.
                        data1.append(data2)
                except IndexError:
                    break

            for i in data1:
                text = i + ' '
                print("i는 머가 나올까요????")
                print(i) # i도 똑같이 data2와 나온다.
                stdout.write(text)

        global line   # 문제 지문
        global line1  # 보기 1번
        global line2  # 보기 2번
        global line3  # 보기 3번
        global line4  # 보기 4번

        with open(route + name, "r") as stdout:
            first_line = stdout.readline()
            want_text = re.split(' 1 | 2 | 3 | 4 ', first_line)

            line = want_text[0].split('. ')[1]
            line1 = want_text[1]
            line2 = want_text[2]
            line3 = want_text[3]
            line4 = want_text[4]


        with open(route + name, "w") as stdout:
            stdout.write(line + '\n')
            stdout.write(line1 + '\n')
            stdout.write(line2 + '\n')
            stdout.write(line3 + '\n')
            stdout.write(line4)
            url_items = "http://192.168.56.1:5000/add"
            data = {'text' : line}
            # global response
            response = requests.post(url_items, json=data)
            global response_data # 딥러닝 서버로부터 세션 번호를 받는 역할
            response_data = response.text
            print(response_data)
            print(response.text)
            print("마지막 line은 머가 나오는지???")
            print(line)

        return redirect('reco:compare')
    return render(request, 'recommend/similarupload.html')

# 문제 출력해주는 곳
@login_required(login_url='accounts:login')
def compare(request):
    global response_data  # 문제 세션 번호
    global count  # 문제 개수
    if 'gettext' in request.POST:
        url_items = "http://192.168.0.19:5000/add"
        text = str(request.POST['gettext'])
        print(text)
        data = {'text': text}
        response = requests.post(url_items, json=data)
        response_data = response.text
        print(response_data)
        print(response.text)
        count = 5
        get_number = response_data  # 딥러닝 서버로부터 받은 과목번호 1 ~ 16
        exercise = DeepExercise.objects.filter(session_number=get_number).order_by('?')[0:count]
        return render(request, 'recommend/similartest.html', {'exercise': exercise})


    get_number = response_data  # 딥러닝 서버로부터 받은 과목번호 1 ~ 16
    exercise = DeepExercise.objects.filter(session_number=get_number).order_by('?')[0:count]
    print(exercise)
    return render(request, 'recommend/similartest.html', {'exercise' : exercise})


# 문제 출력해주는 곳
# @login_required(login_url='accounts:login')
# def compare_test(request):
#     global response_data # 문제 세션 번호
#     global count # 문제 개수
#     get_number = response_data # 딥러닝 서버로부터 받은 과목번호 1 ~ 16
#     DB_que = DeepExercise.objects.filter(session_number=get_number).order_by('?')[0:count]
#     print(DB_que)
#
#     que_id = []
#     questions = []
#     que_FK = []
#     item_contents = []
#     count_list = []
#     num_count = 1
#     if request.method == 'GET':
#
#
#         print(gdivision)
#         DB_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)
#
#         questions = []
#         que_FK = []
#         item_contents = []
#         count_list = []
#         count = 0
#
#         for i in DB_que:
#             question = PREVIOUS_EXERCISE_QUES.objects.filter(PK_ID=i.QUE_ID)
#             for j in question:
#                 questions.append(j.PRE_EXE_QUES_QUESTION)
#                 que_FK.append(j.PK_ID)
#             # questions.append(i.PRE_EXE_QUES_QUESTION)
#             count += 1
#
#         for i in que_FK:
#             item1 = []
#             content = PREVIOUS_EXERCISE_EXAM.objects.filter(FK_PREVIOUS_EXERCISE_QUES=i)
#             for j in content:
#                 if j.PRE_EXAM_NUM == 1:
#                     item1.append(j.PRE_EXAM_SUBSTANCE)
#                 elif j.PRE_EXAM_NUM == 2:
#                     item1.append(j.PRE_EXAM_SUBSTANCE)
#                 elif j.PRE_EXAM_NUM == 3:
#                     item1.append(j.PRE_EXAM_SUBSTANCE)
#                 elif j.PRE_EXAM_NUM == 4:
#                     item1.append(j.PRE_EXAM_SUBSTANCE)
#             item_contents += [item1]
#
#         answer_que = PREVIOUS_EXERCISE_EXAM_ANSWER.objects.filter(DIVISION=gdivision)
#
#         answer_que_list = []
#         for i in answer_que:
#             answer_que_list.append(i.ANSWER_CHECK)
#
#         problem_list = []
#         problem = []
#
#         for i in range(1, 11):
#             count_list.append(i)
#
#         for i, j, k, z in zip(questions, item_contents, count_list, answer_que_list):
#             problem = [i] + j + [k] + [z]
#             problem_list.append(problem)
#
#         # print(problem_list)
#
#         # page = request.GET.get('page', '1')
#         # paginator = Paginator(DB_que, '6')
#         # page_obj = paginator.get_page(page)
#
#         page = request.GET.get('page', '1')
#         paginator = Paginator(problem_list, '6')
#         page_obj = paginator.get_page(page)
#
#         # context = {'question_list' : page_obj}
#
#         # return render(request, 'omrtest.html', context)
#         return render(request, 'extest/omrtest.html',{'page_obj': page_obj, 'count': count_list, 'answer_que': answer_que_list})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password

from django.apps import apps

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str

# 임시 비밀번호 사용
import string
import random


# Create your views here.

def email(request):
    return render(request, 'accounts/email_check.html')

# 로그인 부분
def login(request):
    if request.method == 'POST':
        username = request.POST['username']  # 아이디를 입력받는다.
        password = request.POST['password']  # 비번을 입력받는다.
        user = auth.authenticate(request, username=username, password=password)  # 아이디와 비번을 가져와서 확인한다.
        try:
            if user.is_active == False:
                messages.warning(request, '이메일 인증 후 로그인 해주세요.')
                return render(request, 'accounts/login.html')
        except:
            print("a")
        if user is not None:  # 로그인 부분
            if user.is_active == False:
                messages.warning(request, '이메일 인증 후 로그인 해주세요.')
                return render(request, 'accounts/login.html')
            auth.login(request, user)
            return redirect('main:home')  # 아이디 비번 맞으면 다른곳으로 들어감
        else:  # 아이디 비번 틀렸을 때
            messages.warning(request, '아이디 또는 비밀번호가 틀렸습니다.')
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


# 로그아웃 부분
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


# 회원가입
def signup(request):
    if request.method == 'POST':
        if len(request.POST['username']) == 0:
            messages.warning(request, '아이디를 입력해주세요.')
            return render(request, 'accounts/signup.html')
        elif len(request.POST['password1']) == 0:
            messages.warning(request, '비밀번호를 입력해주세요.')
            return render(request, 'accounts/signup.html')
        elif len(request.POST['email']) == 0:
            messages.warning(request, '이메일을 입력해주세요.')
            return render(request, 'accounts/signup.html')
        elif len(request.POST['last_name']) == 0:
            messages.warning(request, '이름을 입력해주세요.')
            return render(request, 'accounts/signup.html')
        elif len(request.POST['first_name']) == 0:
            messages.warning(request, '닉네임을 입력해주세요.')
            return render(request, 'accounts/signup.html')

        if User.objects.filter(username=request.POST['username']).exists():  # 아이디 중복 체크
            messages.warning(request, '중복된 아이디 입니다.')
            return render(request, 'accounts/signup.html')
        elif User.objects.filter(email=request.POST['email']).exists():  # 이메일 중복 체크
            messages.warning(request, '중복된 이메일 입니다.')
            return render(request, 'accounts/signup.html')
        elif User.objects.filter(first_name=request.POST['first_name']).exists():  # 닉네임 중복 체크
            messages.warning(request, '닉네임을 입력해주세요.')
            return render(request, 'accounts/signup.html')

        if request.POST['password1'] == request.POST['password2']:  # 비번 같은지 체크
            user = User.objects.create_user(  # 새로운 학습자를 만들어서 DB에 저장되는것이다.
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'])
            user.is_active = False # 유저 비활성화
            user.save()
            current_site = get_current_site(request)
            print(current_site)
            print(current_site.domain)
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "AYU 계정 인증 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()

            Alert = apps.get_model('mypage', 'Alert')
            content = request.POST['last_name'] + '님 회원가입을 축하드립니다.'
            alert_add = Alert.objects.create(content=content, user=user)
            alert_add.save()

            messages.warning(request, '회원가입이 완료되었습니다.\n이메일에서 계정을 활성화 시켜주세요.')
            return redirect('accounts:email')
        else:
            messages.warning(request, '비밀번호가 다릅니다.')
            return render(request, 'accounts/signup.html')
        return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')

# 계정 활성화
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return redirect('accounts:login')
        return JsonResponse({"message": "AUTH FAIL"}, status=400)
    except ValidationError:
        return JsonResponse({"message": "TYPE_ERROR"}, status=400)
    except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

# 회원 탈퇴 기능
@login_required(login_url='accounts:login')
def delete(request):
    user = request.user
    if request.method == 'POST':
        print(request.POST['password'])
        if check_password(request.POST['password'], user.password):  # 비밀번호 같은지 체크
            request.user.delete()
            auth.logout(request)  # 세션 지워주기
            return redirect('accounts:login')
        else:
            messages.warning(request, '옳지않은 비밀번호입니다.')
            return render(request, 'main/main.html')
    return redirect('accounts:login')


# 회원 수정 기능
@login_required(login_url='accounts:login')
def member_modify(request):
    if request.method == 'POST':
        user = request.user

        # 아이디 중복
        try:
            user.username == request.POST['username']
        except:
            if User.objects.filter(last_name=request.POST['username']).exists():  # 닉네임 중복 체크
                messages.warning(request, '중복된 닉네임 입니다.')
                return render(request, 'accounts/member_modify.html')

        # 닉네임 중복
        try:
            user.first_name == request.POST['first_name']
        except:
            if User.objects.filter(last_name=request.POST['first_name']).exists():  # 닉네임 중복 체크
                messages.warning(request, '중복된 닉네임 입니다.')
                return render(request, 'accounts/member_modify.html')

        # 이메일 중복
        try:
            user.email == request.POST['email']
        except:
            if User.objects.filter(username=request.POST['email']).exists():  # 이메일(아이디) 중복 체크
                messages.warning(request, '중복된 이메일 입니다.')
                return render(request, 'accounts/member_modify.html')

        try:
            user = auth.authenticate(request, username=user.username, password=request.POST['password1'])
        except:
            messages.warning(request, '비밀번호가 틀렸습니다.')
            return render(request, 'accounts/member_modify.html')
        user.username = request.POST["username"]
        user.first_name = request.POST["first_name"]
        user.email = request.POST["email"]
        user.save()
        return redirect('main:home')
    return render(request, 'accounts/member_modify.html')


# 아이디 찾기
def find_id(request):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        email = request.POST['email']

        try:
            user = User.objects.get(last_name=last_name, email=email)  # 아이디와 비번을 DB로 부터 가져와서

            if user is not None:  # 아이디의 존재를 확인해서 아이디를 가르쳐줌.
                message = render_to_string('accounts/send_id_email.html', {
                    'user': user
                })
                mail_title = "AYU 시스템 아이디 안내 이메일입니다."
                email = EmailMessage(mail_title, message, to=[user.email])
                email.send()
                messages.warning(request, '해당 이메일에 아이디를 전송했습니다.')
                return redirect('accounts:login')
        except:
            messages.warning(request, '이메일 또는 이름이 존재하지 않습니다.')
            return render(request, 'accounts/forgot-id.html')
    return render(request, 'accounts/forgot-id.html')


# 비번 찾기
def find_pw(request):
    if request.method == 'POST':
        email = str(request.POST['email'])
        print(email)
        try:
            user_find_pw = User.objects.get(email=email)
            if user_find_pw is not None:
                new_pw_len = 7  # 새 비밀번호 길이
                pw_candidate = string.ascii_letters + string.digits
                new_pw = ""  # 임시 비밀번호
                for i in range(new_pw_len):
                    new_pw += random.choice(pw_candidate)
                user = User.objects.get(email=email)
                message = render_to_string('accounts/send_pw_email.html', {
                    'user': user,
                    'new_pw': new_pw
                })
                mail_title = "AYU 시스템 임시 비밀번호 안내 이메일입니다."
                email = EmailMessage(mail_title, message, to=[email])
                email.send()
                user_find_pw.set_password(new_pw)
                user_find_pw.save()
                messages.info(request, '임시 비밀번호를 전송해드렸습니다.')
                return redirect('accounts:login')
        except:
            messages.warning(request, '존재하지 않는 이메일입니다.')
            return render(request, 'accounts/forgot-password.html')
    return render(request, 'accounts/forgot-password.html')


# 비번 바꾸기
@login_required(login_url='accounts:login')
def change_pw(request):
    context = {}
    user = request.user
    if request.method == "POST":
        user_password = request.POST['nowpassword']
        user_check = auth.authenticate(request, username=user.username, password=user_password)
        if user_check is not None:
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user_check.set_password(new_password)
                user_check.save()
                return redirect("accounts:login")
            else:
                messages.warning(request, '두개의 새 비밀번호가 일치하지 않습니다.')
                return render(request, 'accounts/change_pw.html')
        else:
            messages.warning(request, '기존의 비밀번호가 맞지 않습니다.')
            return render(request, 'accounts/change_pw.html')
    return render(request, "accounts/change_pw.html", context)

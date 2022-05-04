from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import request
from users.models import *
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth import get_user_model
import json

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .token import users_activation_token


#messages 출력하기위해
from django.contrib import messages
from tkinter import Button, messagebox


# 홈 #

def home(request):
    return HttpResponse('<u>Home</u>')



def back(request):
    return HttpResponse('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><font size ="10"><p><hi><center><b><u>아래 사이트를 클릭 후 재로그인해주세요.</u><br> -Petdada- <br> <font size ="15"><a href="/member/login/">LOGIN</a>')   



from django.views.generic import View

# 회원가입 약관동의

# class AgreementView(View):
#     def get(self, request, *args, **kwargs):
#         request.session['agreement'] = False
#         return render(request, 'users/agreement.html')

#     def post(self, request, *args, **kwarg):
#         if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
#             request.session['agreement'] = True
#             if request.POST.get('register') == 'register':       
#                 return redirect("users:signup")
#         else:
#             messages.info(request, "약관에 모두 동의해주세요.")
#             return render(request, 'users/agreement.html')   

class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.POST['agreement'] = False
        return render(request, 'users/agreement.html')
   
    # def post(self, request, *args, **kwarg):
    #     if request.POST['agreement1'] ==request.POST['agreement2']:   
    #         request.POST['agreement'] = True
    #         if request.POST.get('register') == 'register':       
    #             return redirect("users:signup")
    #     else:
    #         messages.info(request, "약관에 모두 동의해주세요.")
    #         return render(request, 'users/agreement.html')   


#회원가입#

def signup(request):
    user_db = User.objects.all()
    if request.method=="POST":
        if user_db.filter(username=request.POST['username']).exists(): #아이디 중복 체크
            messages.warning(request, "ID already exists")
            return redirect("users:signup")
        if request.POST['confirm_password'] ==request.POST['password']:   
            username=request.POST["username"] #아이디
            password=request.POST["password"] #비밀번호
            email=request.POST["email"] #이메일
            allergyinfo=request.POST.getlist("test_list","allergy") #알레르기 test_list
            address = request.POST["address"] # 주소

            users_user=User.objects.create_user(username,email,password) 
            users_user.allergyinfo = json.dumps(allergyinfo, ensure_ascii = False)
            users_user.address = address
            users_user.is_active = False
            users_user.nickname = username
            users_user.save()

            current_site = get_current_site(request) 
            message = render_to_string('activation.html', {
                'user': users_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(users_user.pk)),
                'token': users_activation_token.make_token(users_user),
            })
            mail_title = "계정 본인확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            #return render(request,"signup2.html")
        else:
            messages.warning(request, 'Password do not match.')
            return redirect("users:signup")
            
    
    return render(request,"login.html")


def validate_email(email):
    if not '@' in email or not '.' in email:
        raise ValidationError(("Invalid Email"), code = 'invalid')

# 이메일 인증 ( 계정 활성화 )
def activate(request, uid64, token ,*args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        users_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        users_user = None
    if users_user is not None and users_activation_token.check_token(users_user, token):
        users_user.is_active = True
        users_user.save()
        auth.login(request, users_user)
        return redirect("/users/login")
    else:
        return render(request, 'home.html', {'error' : '계정 활성화 오류'})
    return 



# 로그인 #

def login(request):
    # 포스트 
    if request.method == 'POST':
        # 정보 가져와서 
        username = request.POST['username']
        password = request.POST['password']
        
        
        # 로그인
        user = auth.authenticate(request, username=username, password=password)
        print(user)

        # 성공
        if user is not None:
            auth.login(request, user)
            request.session['id'] = user.id
            return redirect('/mainpage/mainpage/')
        # 실패
        else:
            messages.warning(request, "Please check your ID and password or check your email.")
            return redirect("users:login")
            #return render(request, 'member/error.html',  {'error': 'username or password is incorrect.'}))
    else:
        return render(request, 'login.html')



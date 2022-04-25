from django.http import HttpResponse
from django.shortcuts import redirect, render
from users.models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    form = UserForm(request.POST)
    return render(request, 'mypage/mywrite_page.html', {'form':form})

# 사용자정보 확인/수정
# 데코레이터 : 로그인 된 사용자에게만 제공되는 페이지에 로그인하지 않은 사용자가 접근하였을 때, 로그인 페이지로 연결되는 기능
@login_required
def user_info(request):
    id = request.session['id']
    tmp = User.objects.get(id=id)
    print(tmp.first_name)
    
    if request.method == 'POST':
        print("POST 동작")
        form = UserUpdateForm(request.POST, instance=request.user)
        print('닉네임: ', request.user.nickname)
        print("valid: ", form.is_valid())
        if form.is_valid():
            print("데이터 수정")
            form.save()
    
    form = UserForm(instance=request.user)
    return render(request, 'mypage/mypage.html', {'form':form})
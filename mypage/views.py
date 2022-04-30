from django.http import HttpResponse
from django.shortcuts import redirect, render
from users.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import json
from django.contrib import auth
from django.contrib import messages

# Create your views here.
def test(request):
    tmp = {
        'tmp':'탈퇴'
    }
    return render(request, 'mypage/withdrawal.html', {'tmp':tmp})

def home(request):
    form = UserForm(request.POST)
    return render(request, 'mypage/mywrite_page.html', {'form':form})

# 사용자정보 확인/수정
# 데코레이터 : 로그인 된 사용자에게만 제공되는 페이지에 로그인하지 않은 사용자가 접근하였을 때, 로그인 페이지로 연결되는 기능
@login_required
def user_info(request):
    id = request.session['id']
    user_get = User.objects.get(id=id)
    print(user_get.first_name)

    checkbox_allergy = ["달걀", "우유", "땅콩", "생선", "갑각류"]
    checkbox_boolean = {
        0:'unchecked',
        1:'unchecked',
        3:'unchecked',
        4:'unchecked',
        5:'unchecked'
    }
    tmp = json.loads(user_get.allergyinfo)
    form_allergy = []
    for i in tmp:
        if i not in checkbox_allergy:
            form_allergy.append(i)
        else:
            idx = checkbox_allergy.index(i)
            print(i, idx)
            checkbox_boolean[idx] = 'checked'

    if request.method == 'POST':
        print("POST 동작", request.POST)
        # 닉네임 설정
        form = UserUpdateForm(request.POST, instance=request.user)
        print('닉네임: ', request.user.nickname)

        # 정보 수정
        if "update" in request.POST:
            # 알레르기 설정
            allergy_list = request.POST.getlist('allergyinfo')
            try:
                allergy_list.remove('None')
            except:
                pass
            print('알레르기: ', allergy_list)

            print("valid: ", form.is_valid())
            if form.is_valid():
                print("데이터 수정")
                temp = form.save(commit=False)
                temp.allergyinfo = json.dumps(allergy_list, ensure_ascii = False)
                temp.save()

        # 회원 탈퇴
        if "bt_delete" in request.POST:
            print(request.POST)
            password_form = CheckPasswordForm(request.user, request.POST)
            print("회원탈퇴")
            if password_form.is_valid():     
                messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/users/login/')

            # if password_form.is_valid():
            #     temp = form.save(commit=False) 
            #     temp.nickname = "탈퇴한 회원"   
    
    form = UserForm(instance=request.user)
    password_form = CheckPasswordForm(request.user)
    return render(
        request, 
        'mypage/mypage.html', 
        {
        'form':form,
        'allergy':form_allergy,
        'check_boolean': checkbox_boolean,
        'password_form':password_form,
        })

# 내가 쓴 글 목록
@login_required
def show_writeList(request):
    id = request.session['id']
    write = Communityboard.objects.filter(userid=id)
    print(request.user.first_name)
    context = {
        "write":write,
    }

    return render(
        request,
        'mypage/mywrite_page.html',
        context
    )
    
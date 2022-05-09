from django.shortcuts import redirect, render
from users.models import *
from mainpage.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import json

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

    checkbox_allergy = ["달걀", "우유", "땅콩", "생선", "새우"]
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
        print('닉네임: ', request.user.nickname)

        # 정보 수정
        if "update" in request.POST:
            # 알레르기 설정
            form = UserUpdateForm(request.POST, instance=request.user)
            allergy_list = request.POST.getlist('allergyinfo')
            try:
                allergy_list.remove('None')
            except Exception:
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
            user_get.is_active = False
            user_get.first_name = 'Unknown'
            user_get.nickname = '탈퇴한 회원'
            user_get.allergyinfo = 'Unknown'
            user_get.email = 'Unknown@Unknown'
            user_get.address = 'Unknown'
            user_get.save()

            return redirect('/users/login/')
    
    form = UserForm(instance=request.user)
    return render(
        request, 
        'mypage/mypage.html', 
        {
            'form':form,
            'allergy':form_allergy,
            'check_boolean': checkbox_boolean,
        }
    )

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

# 내가 좋아요한 레시피글 목록
@login_required
def show_likeList(request):
    id = request.session['id']
    like = Userrecommendedcommunity.objects.filter(userid=id)
    print(request.user.first_name)
    context = {
        "like":like,
    }
    return render(
        request,
        'mypage/like_page.html',
        context
    )

@login_required   
def show_bookmark(request):
    id = request.session['id']
    mark = Userbookmarkrecipe.objects.filter(userid=id)
    print(request.user.first_name)
    context = {
        "mark":mark,
    }
    return render(
        request,
        'mypage/bookmark.html',
        context
    )

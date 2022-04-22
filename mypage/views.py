from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *

# Create your views here.
def home(request):
    form = UserForm(request.POST)
    return render(request, 'mypage/mywrite_page.html', {'form':form})

# 사용자정보 확인/수정
def user_info(request):
    # id = request.session['id']
    id = 1
    tmp = User.objects.get(userid=id)
    content = User.objects.filter(userid=id)
    print(tmp.name)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=tmp)
        if form.is_valid():
            form.save()
    else:
        form = UserForm(instance=tmp)
    return render(request, 'mypage/mypage.html', {'form':form})

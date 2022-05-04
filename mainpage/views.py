from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from users.models import *
from django.contrib.auth.decorators import login_required
import json
from django.contrib import auth
from django.contrib import messages


# Create your views here.
def main(request):
    return render(request, 'mainpage/mainpage.html')

def weather_recomm(request):
    return render(request, 'mainpage/weather_recom.html')

def ingred_recomm(request):
    return render(request, 'mainpage/recipe_recom.html')

def recipe_search(request):
    return render(request, 'mainpage/recipe_search.html')

def ingred_result(request):
    return render(request, 'mainpage/ingredients_result.html')

def ingred_change(request):
    return render(request, 'mainpage/ingredients_change.html')

# 레시피 상세페이지
def recipe_detail(request, recipe_id):
    cookTime = {
        "1":"5",
        "2":"10",
        "3":"15",
        "4":"20",
        "5":"30",
        "6":"60"
    }
    id = request.session['id']
    recipe = recipe_data.objects.filter(recipe_id=recipe_id)[0]
    cook_time = cookTime[recipe.cook_time]
    explain = []
    tmp = recipe.explan
    tmp = tmp.strip('[]').split(',')
    for x in tmp:
        x = x.rstrip("'")
        x = x.lstrip("'")
        x = x.replace(".", "\n")
        print(x)
        explain.append(x)

    context = {
        "recipe":recipe,
        "cook_time":cook_time,
        'explain':explain,
    }

    return render(
        request,
        'mainpage/recipe_detail.html',
        context
    )
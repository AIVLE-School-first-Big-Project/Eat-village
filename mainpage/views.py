from django.shortcuts import render, redirect
from django.http import HttpResponse
from recipe.models import *
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
def recipe_detail(request):
    # id = request.session['id']
    # recipe = recipe_data.objects.filter(recipe_id=recipe_id)
    # context = {
    #     "recipe":recipe,
    # }

    return render(
        request,
        'mainpage/recipe_detail.html',
        # context
    )
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def main(request):
    return render(request, 'mainpage/mainpage.html')

def weather_recomm(request):
    return render(request, 'mainpage/weather_recom.html')

def ingred_recomm(request):
    return render(request, 'mainpage/recipe_recomm.html')

def recipe_search(request):
    return render(request, 'mainpage/recipe_search.html')
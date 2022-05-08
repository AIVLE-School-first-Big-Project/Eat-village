from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from mainpage import recommend_ml
from glob import glob
import re
from numpy import rec
# Create your views here.
# import recommend_ml as rc
# from recipe.models import *
from users.models import *
from django.contrib.auth.decorators import login_required
import json
from django.contrib import auth
from django.contrib import messages
from django.db.models import Q
import random

user_ingre = ['짜왕','버섯','양파','스팸','옥수수']
# Create your views here.

@login_required
def main(request):
    # 북마크 알림 - 지희

    id = request.session['id']
    
    if request.method == "POST":
        form = Userbookmarkrecipe.objects.get(
            userid=id, 
            recipeid=request.POST.get("update_recipeActive", None)
        )
        form.is_active = 1
        form.save()

    bookmark = Userbookmarkrecipe.objects.filter(userid=id, is_active=0)

    # 찬호
    recipes = recipe_data.objects.all()
    recipe_list = []
    for recipe in recipes:
        temp = {'name': recipe.title, 'category1': recipe.category_1, 'category2': recipe.category_2, 'num': recipe.num, 'recipe_id': recipe.recipe_id}
        recipe_list.append(temp)
    
    recipe_list_json = json.dumps(recipe_list)

    context = {
        "update":bookmark,
        'recipes': recipe_list_json
    }
    return render(request, 'mainpage/mainpage.html', context)

@login_required    
def ingred_recomm(request): # 레시피를 추천해주는 코드
    # local 추가한 데이터를 받아온다.
    if request.method == 'GET': 
        print("get")
        storage = request.GET['storage'] 
        data = { 'storage': storage } 
        # return render(request, 'mainpage/recipe_recom.html', data)
    elif request.method == 'POST': 
        print("post")
        storage = request.POST['storage'] 
        data = { 'storage': storage }
        # return render(request, 'mainpage/recipe_recom.html', data)
        
    print("abc")
    
    # 세션의 유저 알러지 데이터를 가져온다. 
    id = request.session['id']
    user_get = User.objects.get(id=id)
    
    # print(user_get.allergyinfo)
    
    
    
    # detect한 식재료를 가져온다.    
    tmp = json.loads(user_get.allergyinfo)

    # form_allergy = []
    # for i in tmp:
    #     allergy_list.append(i)
    #     print(i)
    # print(allergy_list)
    
    
    
    # mainpage.model의 recipe_data에서 알러지 처리해주고 그 쿼리셋의 인덱스를 받는다
    
    
    # 알러지 데이터를 받아서 DB에서 제외시킨다.
    allergy_recipe_idx = [] # 
    
    
    # a_list = [list for list in recipe_data.object.all()[:10] for t in tmp if t in list.ingre]
    # print(a_list)   
    
    # ---------------------------------------------------------------
    re_data_list = recipe_data.objects.all()
    # global user_ingre
    for a in re_data_list:
        for t in tmp:
            if t in a.ingre: 
                # print(a.ingre)
                allergy_recipe_idx.append(a)

                # print(a.title)
    
    # re_data10 = list(re_data10)
    re_data_list = list(re_data_list)
    
    allergy_recipe_idx = list(set(allergy_recipe_idx))
    # print(allergy_recipe_idx)
    a_sub_b = [x for x in re_data_list if x not in allergy_recipe_idx]
    # print(a_sub_b)
    # print(len(re_data_list))
    # print(len(allergy_recipe_idx))
    # print(len(a_sub_b))
    
    recommend_data = recommend_ml.recommend_recipe(user_ingre,re_data_list)
    
    # ---------------------------------------------------------------
        #   {% for item in re_data %}
        # <h3>{{ item.title }} / {{ item.ingre }} </h3>
        # --------------------------------------------------------------------------------------------------
        # {% endfor %}  
    
    # re_data = recipe_data.objects.exclude(ingre='방울토마토')

    # 전처리 한다.
    # detect : user_ingre , storge : 해야함 
    # allergy : user_get.allergyinfo, db : recipe_data
    
    
    # 1. list = detect 값 + 스토리지 값
    # 2. list2 = 알러지 not in DB
    # 3. view.py에서 recom_recipe = recommend(list,list2)
     
    return render(request, 'mainpage/recipe_recom.html', {'recommend_data' :recommend_data})
    # return render(request, 'mainpage/recipe_recom.html', {'data' : user_ingre})
    # return render(request,'mainpage/ingredients_result.html',{'user_data' : user_data,'recommend' : recommend_data,})
@login_required
def recipe_search(request):

    kw = request.GET.get('kw')

    board_list = list(recipe_data.objects.all().filter(
        Q(title__contains=kw) |
        Q(ingre__contains=kw) |
        Q(explan__contains=kw) |
        Q(tag__contains=kw) |
        Q(category_1__contains=kw) |
        Q(category_2__contains=kw) |
        Q(method__contains=kw)
    ))
    if len(board_list) > 10:
        random_board = random.sample(board_list, 10)
    else:
        random_board = random.sample(board_list, len(board_list))

    context = {'board_list': random_board,
               'kw' : kw
               }

    return render(request, 'mainpage/recipe_search.html', context)

@login_required
def ingred_result(request): # 여기가 추가 데이터 처리하는 페이지
    global user_ingre
    # 당근,사과,오이,양파

    
    user_ingre = list(set(user_ingre))
    # re_data = recipe_data.objects.all()
    # recommend_data = recommend_ml.recommend_recipe(user_data,recipe_data)
    
    return render(request,'mainpage/ingredients_result.html',{'user_data' : user_ingre})
    # return render(request,'mainpage/ingredients_result.html',{'user_data' : user_data,'recommend' : recommend_data,})
    # return render(request, 'mainpage/ingredients_result.html')

@login_required
def ingred_change(request):
    return render(request, 'mainpage/ingredients_change.html')
 
# ------------------------------------------------------------------------------
from django.shortcuts import render
from django.http import StreamingHttpResponse
import yolov5,torch
from yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords, 
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
from deep_sort.deep_sort import DeepSort
from deep_sort.utils.parser import get_config
from time import time

import cv2
from PIL import Image as im
# Create your views here.

print(torch.cuda.is_available())
#load model
model = yolov5.load('yolov5s.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
device = select_device('') # 0 for gpu, '' for cpu
# initialize deepsort
cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort('osnet_x0_25',
                    device,
                    max_dist=cfg.DEEPSORT.MAX_DIST,
                    max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    )
# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names
@login_required
def stream():
    global user_ingre
    
    cap = cv2.VideoCapture('C:/django/Eat-village/media/test.webm')
    # cap = cv2.VideoCapture(1)
    # model.conf = 0.65
    # model.iou = 0.5
    # model.classes = [1,2,3,4,6,7,8,10,11]
    
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
        
        results = model(frame, augment=True)
        # proccess
        annotator = Annotator(frame, line_width=2, pil=not ascii) 
        det = results.pred[0]
        if det is not None and len(det):   
            xywhs = xyxy2xywh(det[:, 0:4])
            confs = det[:, 4]
            clss = det[:, 5]
            outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), frame)
            if len(outputs) > 0:
                for j, (output, conf) in enumerate(zip(outputs, confs)):

                    bboxes = output[0:4]
                    id = output[4]
                    cls = output[5]

                    c = int(cls)  # integer class
                    label = f'{id} {names[c]} {conf:.2f}'
                    annotator.box_label(bboxes, label, color=colors(c, True))
                    # print(c,label) # set 형식으로 받아야한다. 그래야 중복데이터가 안들어 오기 때문이다.
                    
                    label = label.split(' ')
                    # print(label[1])
                    user_ingre.append(label[1]) # user_ingre 데이터에 인식된 값을 추가한다. 이걸로 추천시스템 구현
                    
                    user_ingre = list(set(user_ingre))
                    print(user_ingre)

        else:
            deepsort.increment_ages()

        # print(det)
        im0 = annotator.result()    
        image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
@login_required    
def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
@login_required
# 레시피 상세페이지
def recipe_detail(request, recipe_id):
    # 조리 시간 전처리
    cookTime = {
        "1":"5",
        "2":"10",
        "3":"15",
        "4":"20",
        "5":"30",
        "6":"60"
    }
    id = request.session['id']
    bookmark = ''
    try:
        form = Userbookmarkrecipe.objects.get(recipeid=recipe_id)
        bookmark = True
    except:
        bookmark = False
    # 북마크 기능
    # 0 : 알림 확인 안함 , 1 : 알림 확인
    

    if request.method == "POST":
        uploaded = request.POST.get('bookmark_status', None)
        print("데이터 확인", request.POST)
        print("북마크 상태 : ", uploaded)
        result = ""
        user = User.objects.get(id=id)
        recipe_detail = recipe_data.objects.get(recipe_id=recipe_id)
        
        # QQQQ : 데이터 생성하는 방법 찾기
        try:
            form = Userbookmarkrecipe.objects.get(recipeid=recipe_id)
        except:
            Userbookmarkrecipe.objects.create(
                userid = user,
                recipeid = recipe_detail,
                is_active = 0,
            )
            bookmark = True

        if uploaded == "delete mark":
            form.delete()
            bookmark = False

        result = {
            'bookmark':bookmark,
        }
        return JsonResponse(result)
            
    recipe = recipe_data.objects.filter(recipe_id=recipe_id)[0]
    cook_time = cookTime[recipe.cook_time]
    # 요리 방법 전처리
    explain = []
    tmp = recipe.explan
    tmp = tmp.strip('[]').split("',")
    for x in tmp:
        x = x.rstrip("'")
        x = x.lstrip("'")
        x = x.replace(".", ".\n")
    # print(x)
        explain.append(x)


    context = {
        "recipe":recipe,
        "cook_time":cook_time,
        'explain':explain,
        'bookmark':bookmark,
    }

    return render(
        request,
        'mainpage/recipe_detail.html',
        context
    )






def loading(request): #should be deleted
    return render(request, 'mainpage/loading.html')

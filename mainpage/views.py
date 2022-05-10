from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from mainpage import recommend_ml
from users.models import *
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
import random
from django.http import StreamingHttpResponse
import torch
from yolov5.utils.general import xyxy2xywh
from yolov5.utils.torch_utils import select_device
from yolov5.utils.plots import Annotator, colors
from deep_sort.deep_sort import DeepSort
from deep_sort.utils.parser import get_config

user_ingre = []

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
    global user_ingre
    
    # local 추가한 데이터를 받아온다.
    if request.method == 'GET': 
        print("get")
        storage = request.GET['storage'] 
    elif request.method == 'POST': 
        print("post")
        storage = request.POST['storage'] 
    
    # 추가 재료를 유저 재료의 추가
    add_ingre = storage.split(',')

    
    for i in add_ingre:
        user_ingre.append(i)
        
    user_ingre = list(set(user_ingre))

    # 세션의 유저 알러지 데이터를 가져온다. 
    id = request.session['id']
    user_get = User.objects.get(id=id)
    
    # detect한 식재료를 가져온다.    
    tmp = json.loads(user_get.allergyinfo)
 
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

    a_sub_b = [x for x in re_data_list if x not in allergy_recipe_idx]

    
    recommend_data = recommend_ml.recommend_recipe(user_ingre,a_sub_b)
    
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

ingre_dict = {
    '0':"당근",
    '1':"오이",
    '2':"달걀",
    '3':"마늘",
    '4':"우유",
    '5':"양파",
    '6':"고추",
    '7':"피망",
    '8':"감자",
    '9':"대파",
}
@login_required
def ingred_result(request): # 여기가 추가 데이터 처리하는 페이지
    global user_ingre, ingre_dict
    dir_path = "yolov5\\runs\\detect\\exp\\labels"
    for (root, directories, files) in os.walk(dir_path):
        print("경로")
        for file in files:
            file_path = os.path.join(root, file)
            print("경로",file_path)
            f = open(file_path, 'r')
            tmp = f.read().split()
            print("file", tmp)
            user_ingre.append(tmp[0])
    user_ingre = list(set(user_ingre))
    user_ingre = [ingre_dict[x] for x in user_ingre]
    print("확인",user_ingre)
    
    # 당근,사과,오이,양파

    
    # 유저 알러지 정보
    id = request.session['id']
    user_get = User.objects.get(id=id)
    tmp = json.loads(user_get.allergyinfo)
    
    tmp = ', '.join(tmp)
    
    user_ingre_str =""
    user_ingre = list(set(user_ingre))
    
    user_ingre_str = ', '.join(user_ingre)
        
    # re_data = recipe_data.objects.all()
    # recommend_data = recommend_ml.recommend_recipe(user_data,recipe_data)
    
    return render(request,'mainpage/ingredients_result.html',{'user_data' : user_ingre_str, 'test' : tmp})
    # return render(request,'mainpage/ingredients_result.html',{'user_data' : user_data,'recommend' : recommend_data,})
    # return render(request, 'mainpage/ingredients_result.html')

@login_required
def ingred_change(request):
    return render(request, 'mainpage/ingredients_change.html')
 


import cv2

#print(torch.cuda.is_available())
#load model
#model = yolov5.load('64_100.pt')
# #path = '/some/local/path/pytorch/vision'
# path_hubconfig  = "C:\django\Eat-village\yolov5"
# path_weightfile  = "C:\django\Eat-village\\64_100.pt"
# #model = torch.hub.load(path, 'resnet50', pretrained=True)
# # model = torch.hub.load(path, '64_100', pretrained=False, source='local')
# model = torch.hub.load(path_hubconfig, 'custom',
#                         path=path_weightfile, source='local')
# device = select_device('') # 0 for gpu, '' for cpu
# # initialize deepsort
# cfg = get_config()
# cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
# deepsort = DeepSort('osnet_x0_25',
#                     device,
#                     max_dist=cfg.DEEPSORT.MAX_DIST,
#                     max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
#                     max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
#                     )
# # Get names and colors
# names = model.module.names if hasattr(model, 'module') else model.names

# cl = 0
# conf = 0
import os
from yolov5 import detect
path = os.getcwd()
print(path)



# yolo 실행
import time
def convert():
    # os.system("ffmpeg -i ./media/test.webm ./test/data/test.mp4")
    os.system("ffmpeg -i ./media/test.webm -qscale 0 ./test/data/test.mp4")
    
    # print (os.c)
    
    # file_size = os.stat("./test/data/test.mp4") # 인코딩 하는 파일의 데이터 크기
    # tmp_size = file_size.st_size
    # print(file_size.st_size, tmp_size)
    # while (file_size.st_size != tmp_size):
    #     tmp_size = file_size.st_size
    #     print("파일크기:",tmp_size)
    # print(file_size.st_size)


    return 0

def stream():   
    print("시작")
    cap = cv2.VideoCapture('media/test.webm')
    # cap = cv2.VideoCapture(1)
    # model.conf = 0.65
    # model.iou = 0.5
    # model.classes = [1,2,3,4,6,7,8,10,11]
    print("영상 로드")
    res = convert()
    print(res)
    
    # 파일이 존재하면 다음 코드 진행
    
    
    
    detect.run(
            conf_thres=0.65,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            source= path + '/test/data/test.mp4',
            weights=path + '/test/l_64_50_best.pt',
            name=path + '/test/result',
            imgsz=(416, 416),
            save_txt=True,
            save_conf=True,  # save confidences in --save-txt labels
            save_crop=True,  # save cropped prediction boxes
    )

    
    
    global user_ingre

    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         print("Error: failed to capture image")
    #         break
        
    #     results = model(frame, augment=True)
    #     # proccess
    #     annotator = Annotator(frame, line_width=2, pil=not ascii) 
    #     det = results.pred[0]

    #     if det is not None and len(det):   
    #         xywhs = xyxy2xywh(det[:, 0:4])
    #         confs = det[:, 4]
    #         clss = det[:, 5]
    #         outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), frame)
    #         if len(outputs) > 0:
    #             for j, (output, conf) in enumerate(zip(outputs, confs)):

    #                 bboxes = output[0:4]
    #                 id = output[4]
    #                 cls = output[5]

    #                 c = int(cls)  # integer class
    #                 label = f'{id} {names[c]} {conf:.2f}'
    #                 annotator.box_label(bboxes, label, color=colors(c, True))
    #                 # print(c,label) # set 형식으로 받아야한다. 그래야 중복데이터가 안들어 오기 때문이다.
                    
    #                 label = label.split(' ')
    #                 # print(label[1])
    #                 user_ingre.append(label[1]) # user_ingre 데이터에 인식된 값을 추가한다. 이걸로 추천시스템 구현
                    
    #                 user_ingre = list(set(user_ingre))
    #                 print(user_ingre)

    #     else:
    #         deepsort.increment_ages()

    #     # print(det)
    #     im0 = annotator.result()    
    #     image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')



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
    except Exception:
        bookmark = False
    # 북마크 기능
    # 0 : 알림 확인 안함 , 1 : 알림 확인
    

    if request.method == "POST":
        uploaded = request.POST.get('bookmark_status', None)
        print("북마크 상태 : ", uploaded)
        result = ""
        user = User.objects.get(id=id)
        recipe_detail = recipe_data.objects.get(recipe_id=recipe_id)
        
        try:
            form = Userbookmarkrecipe.objects.get(recipeid=recipe_id)
        except Exception:
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

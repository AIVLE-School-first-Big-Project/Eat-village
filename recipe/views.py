import re

from django.http import HttpResponse
from django.shortcuts import render
from numpy import rec
# Create your views here.
from recipe import recommend_ml
# import recommend_ml as rc
import recipe.models as models
from .models import recipe_data, user_ingre



def insert(request):
    # # 1. create()
    # recipe_data.objects.create(name="테스트",method="튀김은 옳다",category_1="일식",
    #                            category_2 ="튀김", igd="새우,고구마,감자,김말이")
    # # 2. save()
    # r = recipe_data(name="테스트2",method="치킨은 옳다",category_1="한식",
    #                            category_2 ="튀김", igd="새우,고구마,감자,김말이")
    # r.save()
    # # 3-html/css/js 입력
    # recipe_data(name="테스트3",method="구운건 옳다",category_1="양식",
    #                            category_2 ="튀김", igd="새우,고구마,감자,김말이").save()

    # 4-django 입력
    recipe_data(name="테스트4",method="장고는 싫다",category_1="중식",category_2 ="튀김", 
                mgt="존맛탱구리",igd="두부,달걀,양파,감자,소금,후추,표고가루,참기름,통깨", serv="2인분", cook_time="30분이내").save()
    recipe_data(name="테스트1",method="장고 싫어",category_1="한식",category_2 ="볶음", 
                mgt="존맛탱구리",igd="두부,달걀,양파,감자,소금,후추,표고가루,참기름,통깨", serv="1인분", cook_time="20분이내").save()
    
    user_ingre.objects.create(ingre="청국장,두부,호박,홍고추,멸치,생수,간마늘,대파,표고버섯,고춧가루")
    
    return HttpResponse('데이터 입력 완료')

# def show(request):
#     user_data = user_ingre.objects.all()
#     result = ''
#     for r in user_data:
#         result += r.method + '<br>'
#     return HttpResponse(result)

def show(request):
    re_data = recipe_data.objects.all()
    user_data = user_ingre.objects.all()
    test_data = recommend_ml.recommend_recipe(user_ingre,recipe_data)
    return render(request, 'recipe/show.html',{'data' : re_data, 'user' : user_data, 'test' : test_data})



from django.shortcuts import render
from django.http import StreamingHttpResponse
import yolov5,torch
from yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords, 
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
from deep_sort.deep_sort import DeepSort
from deep_sort.utils.parser import get_config

import cv2
from PIL import Image as im
# Create your views here.
def index(request):
    return render(request,'index.html')
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

def stream():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    model.conf = 0.45
    model.iou = 0.5
    model.classes = [0,64,39]
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

        else:
            deepsort.increment_ages()

        im0 = annotator.result()    
        image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame') 
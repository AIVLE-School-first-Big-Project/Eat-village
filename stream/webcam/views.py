from django.http import StreamingHttpResponse
from django.shortcuts import render
import yolov5, torch
from yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords,
                                  check_imshow, xyxy2xywh, increment_path, strip_optimizer, colorstr)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors, save_one_box
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
import cv2
from PIL import Image as im
# Create your views here.

def index(request):
    return render(request, 'index.html')
print(torch.cuda.is_available())
# load model
#model = yolov5.load('yolov5s.pt')
model = torch.hub.load('ultralytics/yolov5','yolov5s')
device = select_device('') # gpu 0 only use cpu

cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort('osnet_x0_25',
                    device,
                    max_dist=cfg.DEEPSORT.MAX_DIST,
                    max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    )
names = model.module.names if hasattr(model, 'module') else model.names


def stream():
    #cap = cv2.VideoCapture(0)
    #cap = cv2.imdecode()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error : failed to capture image")
            break
        
        results = model(frame, augment=True)
        #annotator = Annotator(frame, line_width=2, pil=not ascii)

        for i in results.render():
            data = im.fromarray(i)
            data.save('demo.jpg')
        #cv2.imwrite('demo.jpg',frame)

        #print(results)
        #image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg','rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
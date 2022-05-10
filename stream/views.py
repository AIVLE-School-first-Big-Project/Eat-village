from http.server import executable
from django.http import StreamingHttpResponse
from django.shortcuts import render
import yolov5
import torch
from yolov5.utils.torch_utils import select_device
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
import cv2
from PIL import Image as im
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings 
from .forms import UploadFileForm
import ffmpeg
import sys

def index(request):
    print(request)
    if request.method == 'POST':
        print("ajax 전송 확인")
        print(request.POST)
        print(request.FILES["data"].size)
        file = request.FILES["data"]
        fs = FileSystemStorage()
        if fs.exists('test.webm'):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'test.webm'))
        
        filename = fs.save("test.webm", file)
        print("저장 확인: ", filename)

        # ffmpeg "-i media\test.webm -c copy -strict -2 media\video.mp4"
        # os.system("ffmpeg -i test.webm output.mp3") 
        sys("sudo ffmpeg -i media\test.webm -c copy -strict -2 media\output.mp4")
        # os.system("ffmpeg -i media\test.webm -c -copy \123123.mp4")
        # video_stream = request.FILES["data"]
        
        # with open('file.webm', 'wb') as f_vid:
        #     f_vid.write(base64.b64encode(video_stream))

        # with open('file.webm', 'rb') as f_vid:
        #     video_stream = base64.b64decode(f_vid.read())

        # print(video_stream)
    return render(request, 'stream/index.html')



# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            #return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    #return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('stream/media/test.webm', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

print(torch.cuda.is_available())
# load model
model = yolov5.load('yolov5s.pt')
# model = torch.hub.load('ultralytics/yolov5','yolov5s')
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
    
    cap = cv2.VideoCapture()
    #cap = request.files['image']

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

@csrf_exempt
def video_feed(request):
    if request.method == 'POST':
        print("ajax 전송 확인")
        print(request.POST)
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
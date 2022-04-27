import os
from django.utils.timezone import now

def upload_image(instance, filename):
  # filename_base, filename_ext = os.path.splitext(filename)
  # print(filename_base, filename_ext)  
  return '%s' % (
    now().strftime('%Y%m%d')+"_"+filename
  )
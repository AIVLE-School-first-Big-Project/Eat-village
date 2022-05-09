from django.utils.timezone import now

def upload_image(instance, filename):  
    return '%s' % (
      now().strftime('%Y%m%d')+"_"+filename
    )
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import *

def send_otp_via_email(email):
    subject = 'veridication'
    otp = random.randint(1000 ,9999)
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject , message , email_from , [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp 
    user_obj.save()

def send_doc(email , pk):
    subject = 'send doc'
    
    #otp = random.randint(1000 ,9999)
    message = f'go there http://127.0.0.1:8000/api/Nursedocumint/{pk}/'
    email_from = settings.EMAIL_HOST
    send_mail(subject , message , email_from , [email])
    # user_obj = Nurse.objects.get(email=email)
    # user_obj.otp = otp 
    # user_obj.save()
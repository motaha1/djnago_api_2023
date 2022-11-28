from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from apis import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('nurse/',views.FBV_nurse ),
    path('patient/',views.FBV_patiant ),
    path('users/',views.FBV_user_get ),
    path('nurse/<pk>/',views.FBV_nurse_pk),
    path('tokenrequest/' , obtain_auth_token),
    path('patient/<pk>/',views.FBV_patiant_pk),
    path('login/',views.FBV_login),
    path('otp/',views.otp_verify),
    path('Nursedocumint/<pk>/' ,views.mainview.as_view() , name='main-view') , 
    path('Nursedocumint/<pk>/upload' ,views.file_upload , name='upload')

    
    
    




   

]


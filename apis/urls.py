from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from apis import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('nurse/',views.FBV_List ),
    path('patient/',views.FBV_patiant ),
    path('users/',views.FBV_user_get ),
    path('nurse/<pk>/',views.FBV_pk ),
    path('tokenrequest/' , obtain_auth_token),




   

]
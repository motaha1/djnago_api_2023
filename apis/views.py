from lib2to3.pgen2 import token
from django.shortcuts import render
from django.http.response import JsonResponse

from apis.emails import send_otp_via_email
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist


#from .permissions import IsAuthorOrReadOnly



#1 without REST and no model query FBV
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            "Name": "Omar",
            "mobile": 789456,
        },
        {
            'id': 2,
            'name': "yassin",
            'mobile': 74123,
        }
    ]
    return JsonResponse (guests, safe=False)

# #2 model data default djanog without rest
# def no_rest_from_model(request):
#     data = Guest.objects.all()
#     response = {
#         'guests': list(data.values('name','mobile'))
#     }
#     return JsonResponse(response)


# List == GET
# Create == POST
# pk query == GET 
# Update == PUT
# Delete destroy == DELETE

#3 Function based views 
#3.1 GET POST
@api_view(['GET','POST'])

def FBV_nurse(request):
    # GET
    if request.method == 'GET':
        nurse = Nurse.objects.all()
        serializer = NurseSerializer(nurse, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        data =request.data
        user = User.objects.create(username = data['username'] , password = data['password'] , is_Nurse = True)
        nurse = Nurse.objects.create(user= user , mobile = data['mobile'], city = data['city'] )
        Token.objects.create(user = user)
        

       
        return Response(status= status.HTTP_201_CREATED)
        

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_nurse_pk(request, pk):
    try:
       nurse = Nurse.objects.get(pk=pk)
    except Nurse.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = NurseSerializer(nurse)
        return Response(serializer.data)
        
    # PUT
    elif request.method == 'PUT':
        serializer = NurseSerializer(nurse, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        nurse.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

################################################user##############################33

#3.1 GET POST
@api_view(['GET','POST'])

def FBV_user_get(request):
    # GET
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        data =request.data
        user = User.objects.create(username = data['username'] , password = data['password'] , is_Nurse = True)
        Token.objects.create(user)
        

       
        return Response(status= status.HTTP_201_CREATED)
        

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_user_put(request, pk):
    try:
       nurse = Nurse.objects.get(pk=pk)
    except Nurse.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = NurseSerializer(nurse)
        return Response(serializer.data)
        
    # PUT
    elif request.method == 'PUT':
        serializer = NurseSerializer(nurse, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        nurse.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


##############################################################################################
#patiant

@api_view(['GET','POST'])

def FBV_patiant(request):
    # GET
    if request.method == 'GET':
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient, many=True)
        return Response(serializer.data)

    # POST
    elif request.method == 'POST':
        data1= {}
        data =request.data
        user = User.objects.create( email = data['email'] , password = data['password'] ,  is_Patient = True)
        patient = Patient.objects.create(user= user , mobile = data['mobile'], city = data['city'] , gender = data['gender'] )
        Token.objects.create(user = user)
        send_otp_via_email(data['email'])
        data1['response'] = 'ok'
        data1['token'] = Token.objects.get(user =user).key

        

       
        return Response(data1)
        

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_patiant_pk(request, pk):
    try:
       patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
        
    # PUT
    elif request.method == 'PUT':
        serializer = NurseSerializer(patient, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        patient.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


###########################login#######################################

@api_view(['POST'])
def FBV_login(request):
    try:
        pk1 = request.data['pk1']
        pk2 = request.data['pk2']
        user = User.objects.get(email = pk1 , password = pk2)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'POST':
        data = {}

        data['responce'] = 'ok'
        data['type'] = 'patient'
        data['token'] = Token.objects.get(user=user).key
        if (user.is_Patient == True):
            patient = Patient.objects.get(user = user)
            serializer = PatientSerializer(patient)
            response = dict (data)
            response.update(serializer.data)

            

            return Response(response)


#########################################otp_verify############################################3

@api_view(['POST'])
def otp_verify(request):
    try:
        email = request.data['email']
        otp = request.data['otp']
        user = User.objects.get(email = email)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    if request.method == 'POST':
        if user.otp == otp :
            
            user.is_verified = True
            data = {}
            data['responce'] = 'ok'
            data['token'] = Token.objects.get(user=user).key
            data['message'] = 'its verify'


            return Response(data)
        
        else:
            return Response(
             {
                'responce' : 'otp wrong'
             }

            )







            
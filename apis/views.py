from lib2to3.pgen2 import token
from django.shortcuts import render
from django.http.response import JsonResponse

from apis.emails import send_doc, send_otp_via_email
from apis.firebase import firebase_sigup
from apis.firestore import addpatient_firestore

from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404 , HttpResponse
from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist




import pandas as pd
# from math import sqrt
import numpy as np
# import matplotlib.pyplot as plt


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
        user = User.objects.create(email = data['email'] , password = data['password'] , is_Nurse = True)
        nurse = Nurse.objects.create(user= user , mobile = data['mobile'], city = data['city'] )
        #send_otp_via_email(data['email'])
        send_doc(data['email'] , nurse.pk)
        Token.objects.create(user = user)
        

       
        return Response(status= status.HTTP_201_CREATED)
        


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
        nurse_user = User.objects.get(id=nurse.user.id)
        nurse_user.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

################################################user##############################33


@api_view(['GET'])

def FBV_user_get(request):
    # GET
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    # # POST
    # elif request.method == 'POST':
    #     data =request.data
    #     user = User.objects.create(username = data['username'] , password = data['password'] , is_Nurse = True)
    #     Token.objects.create(user)
        

       
    #     return Response(status= status.HTTP_201_CREATED)
        


@api_view(['GET','PUT'])
def FBV_user_pk(request, pk):
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
        try :
            firebase_sigup(data['email'] , data['password'])
            user = User.objects.create( email = data['email'] , password = data['password'] ,  is_Patient = True)
            patient = Patient.objects.create(user= user , mobile = data['mobile'], city = data['city'] , gender = data['gender'] )
            Token.objects.create(user = user)
            send_otp_via_email(data['email'])
            data1['response'] = 'ok'
            data1['token'] = Token.objects.get(user =user).key
            addpatient_firestore(data['email'] , data['name'] , data['city'])
            return Response(data1)
        except :
            return Response({
                "responce":"error"
            })


        


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
        user_patient = User.objects.get(id=patient.user.id)
        user_patient.delete()
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
            ##new##
            user.save()
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


##################################send doc/nurse ######################################
from django.views.generic import TemplateView

class mainview(TemplateView):
    template_name = 'main.html'


def file_upload (request , pk) :

    if request.method =='POST' : 
        my_file =request.FILES.get('file')
        nurse =Nurse.objects.get(pk = pk)
        nurse.doc = my_file
        nurse.save()

        testupload.objects.create(upload =my_file)

        return HttpResponse('upload')

    return HttpResponse('not upload')


################################### rating nurse ######################################


@api_view([ 'POST' , 'GET'])
def rating(request) :


    if request.method =='GET' :
     
        try :
            nurse_id = int (request.data['nurse_id'])
            nurse = Nurse.objects.get(pk = nurse_id) 
        except  :
            return Response({'responce':'error'})
        
        rate = Rating.objects.filter(nurse = nurse)
        serializers =RatingSerializer(rate ,many =True )
        return Response(serializers.data)



    
    if(request.method =='POST'):
         nurse_id= request.data['nurse_id']
         patient_id = request.data['patient_id']
         nurse = Nurse.objects.get(pk = nurse_id)
         patient = Patient.objects.get(pk = patient_id)
        
         try :
           rate =  Rating.objects.create(patient = patient , nurse = nurse)
   
           return Response ({
            'responce'  : 'ok'
           })

         except : 
            return Response (
                {
                    'responce' : "error"
                }
            )


@api_view(['GET','PUT','DELETE'])

def rating_pk (request , pk)  :
    try :
        rate = Rating.objects.get(pk=pk)
    except Rating.DoesNotExist :

        return Response(status=status.HTTP_404_NOT_FOUND)


    if (request.method == 'PUT'):

       data = request.data
       rate.stars = data['stars']
       rate.save()

       return Response({'responce':'ok'})
 
    if (request.method == 'DELETE'):

       
       rate.delete()
       return Response({'responce':'ok'})

    if (request.method == 'GET'):
        serializer = RatingSerializer(rate)
        print(serializer.data)
        return Response(serializer.data)


# @api_view(['GET','PUT','DELETE'])
# def rating_pk(request, pk):
#     try:
#         rate = Rating.objects.get(pk=pk)
#     except Rating.DoesNotExists:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     # GET
#     if request.method == 'GET':
#         serializer = RatingSerializer(rate)
#         return Response(serializer.data)
        
#     # PUT
#     elif request.method == 'PUT':
#         serializer = RatingSerializer(rate, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'responce' , 'ok'})
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#     # DELETE
#     if request.method == 'DELETE':
#         rate.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)



######################## RecommendationSystem #####################################

# def generateRecommendation(request):
#     nurse=Nurse.objects.all()
#     rating=Rating.objects.all()
#     x=[] 
#     y=[]
#     A=[]
#     B=[]
#     C=[]
#     D=[]
#     #Movie Data Frames
#     for item in nurse:
#         x=[item.id,item.name,item.user.email] 
#         y+=[x]
#     movies_df = pd.DataFrame(y,columns=['nurseId','name','email'])
#     print("Nurse DataFrame")
#     print(movies_df)
#     print(movies_df.dtypes)
#     #Rating Data Frames
#     print(rating)
#     for item in rating:
#         A=[item.patient.id,item.nurse,item.stars]
#         B+=[A]
#     rating_df=pd.DataFrame(B,columns=['patientId','nurseId','rating'])
#     print("Rating data Frame")
#     rating_df['paientId']=rating_df['patientId'].astype(str).astype(np.int64)
#     rating_df['nurseId']=rating_df['nurseId'].astype(str).astype(np.int64)
#     rating_df['rating']=rating_df['rating'].astype(str).astype(np.float)
#     print(rating_df)
#     print(rating_df.dtypes)
#     if request.user.is_authenticated:
#         userid=request.user.id
#         #select related is join statement in django.It looks for foreign key and join the table
#         userInput=Rating.objects.select_related('movie').filter(user=userid)
#         if userInput.count()== 0:
#             recommenderQuery=None
#             userInput=None
#         else:
#             for item in userInput:
#                 C=[item.movie.title,item.rating]
#                 D+=[C]
#             inputMovies=pd.DataFrame(D,columns=['name','rating'])
#             print("Watched Movies by user dataframe")
#             inputMovies['rating']=inputMovies['rating'].astype(str).astype(np.float)
#             print(inputMovies.dtypes)

#             #Filtering out the movies by title
#             inputId = movies_df[movies_df['name'].isin(inputMovies['name'].tolist())]
#             #Then merging it so we can get the movieId. It's implicitly merging it by title.
#             inputMovies = pd.merge(inputId, inputMovies)
#             # #Dropping information we won't use from the input dataframe
#             # inputMovies = inputMovies.drop('year', 1)
#             #Final input dataframe
#             #If a movie you added in above isn't here, then it might not be in the original 
#             #dataframe or it might spelled differently, please check capitalisation.
#             print(inputMovies)

#             #Filtering out users that have watched movies that the input has watched and storing it
#             userSubset = rating_df[rating_df['nurseId'].isin(inputMovies['nurseId'].tolist())]
#             print(userSubset.head())

#             #Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
#             userSubsetGroup = userSubset.groupby(['patientId'])
            
#             #print(userSubsetGroup.get_group(7))

#             #Sorting it so users with movie most in common with the input will have priority
#             userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

#             print(userSubsetGroup[0:])


#             userSubsetGroup = userSubsetGroup[0:]


#             #Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
#             pearsonCorrelationDict = {}

#         #For every user group in our subset
#             for name, group in userSubsetGroup:
#             #Let's start by sorting the input and current user group so the values aren't mixed up later on
#                 group = group.sort_values(by='nurseId')
#                 inputMovies = inputMovies.sort_values(by='nurseId')
#                 #Get the N for the formula
#                 nRatings = len(group)
#                 #Get the review scores for the movies that they both have in common
#                 temp_df = inputMovies[inputMovies['nurseId'].isin(group['nurseId'].tolist())]
#                 #And then store them in a temporary buffer variable in a list format to facilitate future calculations
#                 tempRatingList = temp_df['rating'].tolist()
#                 #Let's also put the current user group reviews in a list format
#                 tempGroupList = group['rating'].tolist()
#                 #Now let's calculate the pearson correlation between two users, so called, x and y
#                 Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
#                 Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
#                 Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
                
#                 #If the denominator is different than zero, then divide, else, 0 correlation.
#                 if Sxx != 0 and Syy != 0:
#                     pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
#                 else:
#                     pearsonCorrelationDict[name] = 0

#             print(pearsonCorrelationDict.items())

#             pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
#             pearsonDF.columns = ['similarityIndex']
#             pearsonDF['patientId'] = pearsonDF.index
#             pearsonDF.index = range(len(pearsonDF))
#             print(pearsonDF.head())

#             topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:]
#             print(topUsers.head())

#             topUsersRating=topUsers.merge(rating_df, left_on='patientId', right_on='patientId', how='inner')
#             topUsersRating.head()

#                 #Multiplies the similarity by the user's ratings
#             topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']
#             topUsersRating.head()


#             #Applies a sum to the topUsers after grouping it up by userId
#             tempTopUsersRating = topUsersRating.groupby('nurseId').sum()[['similarityIndex','weightedRating']]
#             tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
#             tempTopUsersRating.head()

#             #Creates an empty dataframe
#             recommendation_df = pd.DataFrame()
#             #Now we take the weighted average
#             recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
#             recommendation_df['nurseId'] = tempTopUsersRating.index
#             recommendation_df.head()

#             recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
#             recommender=movies_df.loc[movies_df['nurseId'].isin(recommendation_df.head(5)['nurseId'].tolist())]
#             print(recommender)
#             return recommender.to_dict('records')

from django.db.models import Avg
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

@api_view(['GET'])
def fake_recommendation_nurse(request , city) :

    if request.method =='GET' :
     
        try :
          
            #n = Nurse.objects.filter(id=3)
            #stars = Rating.objects
            count = Nurse.objects.all().annotate(avg_rating=Avg('rates__stars'))
            count = count.order_by('-avg_rating').values()
            selectedcity = count.filter(city = city)
            notinmycity = count.exclude(city = city)
        except  :
            return Response({'responce':'error'}
            )
        #user_ratings = UserRating.objects.all().values('User_Name').order_by('User_Name').annotate(rating_average=Avg('Rating'))

        map={}
        map1 = {}
      
        for x in selectedcity :

            map[x.name]= str(str(x.avg_rating) + x.city) 
        
        for x in notinmycity :
            map1[x.name]= str(str(x.avg_rating) + x.city) 

        
       
        serializers =NurseSerializer(count , many =True)
        map.update(map1)
        return Response(map)

###################### reset password #############################

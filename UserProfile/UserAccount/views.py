from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
@api_view(['POST']) 
def UserSignupView(request):
   if request.method == 'POST': 
        email=request.data['email']
        password=request.data['password']
        user_email=UserModel.objects.filter(email=email)
        if user_email.exists():
            return Response({"messege":"You are already Registered"},status=status.HTTP_400_BAD_REQUEST)
        
        users=get_user_model().objects.all()
        for user in users:
            if user.check_password(password):
                return Response({"messege":"Password already used"},status=status.HTTP_400_BAD_REQUEST)
        user_obj=UserModel.objects.create(email=email)
        user_obj.set_password(password)
        user_obj.save()
        return Response({"messege":"Account created successfully"},status=status.HTTP_201_CREATED)
    
@api_view(['POST']) 
def LoginView(request):  
    if request.method == 'POST':
        email=request.data['email']
        password=request.data['password'] 
        if UserModel.objects.filter(email=email).exists() :
            u=get_user_model().objects.get(email=email)
            haspassword=u.password
            if check_password(password, haspassword):
                user_obj=authenticate(email=email,password=password)    
                refresh=RefreshToken.for_user(user_obj)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "messege":"Login successfully"
                })
            else:
                return Response({"messege":"Account not found"},status=status.HTTP_400_BAD_REQUEST)        
        else:
            return Response({"messege":"Account not found"},status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['PUT']) 
def CreateProfileView(request):
   if request.method == 'PUT': 
        users=request.user
        if users.is_authenticated: 
            u=UserModel.objects.get(id=users.id)
            serializer=ProfileEditSerializer(u,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"messege":"Profile Updated successfully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors)    
        else:
            raise AuthenticationFailed('Unauthenticated!')
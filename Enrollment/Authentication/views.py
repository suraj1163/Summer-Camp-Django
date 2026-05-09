from django.http import JsonResponse
from django.shortcuts import render
from .models import UserInfo
from .serializers import UsersInfoSerializer
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        if UserInfo.objects.filter(email=email).exists():
            user = UserInfo.objects.get(email=email)

            if user.check_password(password):
                token = Token.objects.create(user=user)
                return JsonResponse({'message':'Login Success',"user":UsersInfoSerializer(user).data,"token":token.key})
            else:
                return JsonResponse({'message':'Invalid Password'})
        else:
            return JsonResponse({'message':'User Not Found'})
        


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_registration(request):
        data = request.data

        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')


        if UserInfo.objects.filter(email=email).exists():
            return JsonResponse({'message':'User Already exist with same email id'})

        else:
            user = UserInfo.objects.create(email=email,first_name=first_name,last_name=last_name,username=username)
            user.set_password(password) # password encrypt
            user.save()
            return JsonResponse({'message':'User Created Successfully'})
        
    




@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    # return JsonResponse({'message':'User Info',"user":UsersInfoSerializer(user).data})
    user_info = UserInfo.objects.get(id=user.id)
    user_data = UsersInfoSerializer(user_info).data
    return JsonResponse({'message':'User Info',"user":user_data})


   

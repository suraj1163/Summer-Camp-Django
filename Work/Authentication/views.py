from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import user_register_serializers, user_login_serializers, user_profile_serializers
from .models import user_register, user_login, user_profile
# Create your views here.

@api_view(['POST'])
def user_register_api(request):
    if request.method == 'POST':
        serializer = user_register_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    users = user_register.objects.all()
    serializer = user_register_serializers(users, many=True)
    return Response({'user_register': serializer.data})

@api_view(['POST'])
def user_login_api(request):
    if request.method == 'POST':
        serializer = user_login_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    users = user_login.objects.all()
    serializer = user_login_serializers(users, many=True)
    return Response({'user_login': serializer.data})

@api_view(['POST'])
def user_profile_api(request):
    if request.method == 'POST':
        serializer = user_profile_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    users = user_profile.objects.all()
    serializer = user_profile_serializers(users, many=True)
    return Response({'user_profile': serializer.data})
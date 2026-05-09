from django.shortcuts import render
from django.http import HttpResponse
from .models import job_create
from .models import job_category
from .models import job_list
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime   
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.

@api_view(['POST'])
def job_category_api(request):
    if request.method == 'POST':
        serializer = serializers.job_category_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    categories = job_category.objects.all()
    serializer = serializers.job_category_serializers(categories, many=True)
    return Response({'job_category': serializer.data})

@api_view(['POST'])
def job_create_api(request):
    serializer = serializers.job_create_serializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def job_list_api(request):
    if request.method == 'POST':
        serializer = serializers.job_list_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    jobs = job_list.objects.all()
    serializer = serializers.job_list_serializers(jobs, many=True)
    return Response({'job_list': serializer.data})

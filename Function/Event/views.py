from django.http import HttpResponse
from Event.models import Event
from Event.models import EventRegistration_list
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@api_view(['GET'])
def Event_list(request):
    return HttpResponse("Event_list")

@api_view(['POST'])
def EventRegistration_list(request):
    return HttpResponse("EventRegistration_list")
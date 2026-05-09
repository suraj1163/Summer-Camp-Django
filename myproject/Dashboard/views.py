from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def dashboard(request):
    return HttpResponse("Welcome to the Dashboard!")

def redeem(request):
    return HttpResponse("Ready TO Redeem")


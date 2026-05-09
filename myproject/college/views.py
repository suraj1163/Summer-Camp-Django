from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def college(request):
    return HttpResponse("Welcome to the College Page!")

def Students(request):
    return HttpResponse("Welcome to the Students Page!")


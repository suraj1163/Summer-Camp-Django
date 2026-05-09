from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import user_register
from Job.models import job_create
from Application.models import user_application, user_application_list
from Application.serializers import user_application_serializers, user_application_list_serializers

# Create your views here.

@api_view(['POST'])
def user_application_api(request):
    if request.method == 'POST':
        serializer = user_application_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    applications = user_application.objects.all()
    serializer = user_application_serializers(applications, many=True)
    return Response({'user_application': serializer.data})

@api_view(['POST'])
def user_application_list_api(request):
    if request.method == 'POST':
        serializer = user_application_list_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    applications = user_application_list.objects.all()
    serializer = user_application_list_serializers(applications, many=True)
    return Response({'user_application_list': serializer.data})

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import StudentsRegistration
from .models import Students
from .models import College
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from datetime import datetime   
from Events.models import Event
# Create your views here.
@api_view(['GET', 'POST'])
@authentication_classes([]) # No token required so it's easy to test
@permission_classes([])
def student_list_api(request):
    if request.method == 'GET':
        # --- Handle GET request ---
        # Get all students from the database and return them
        students = Students.objects.all()
        student_data = []
        for student in students:
            student_data.append({
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "College": student.College
            })
        return Response({"message": "Successfully fetched all students", "data": student_data})

    elif request.method == 'POST':
        # --- Handle POST request ---
        # Get data from Postman body and create a new student
        import json
        data = json.loads(request.body)
        
        new_student = Students.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            age=data.get('age'),
            College=data.get('College')
        )
        return Response({"message": "New student created successfully!", "student_id": new_student.id})

@api_view(['GET', 'POST'])
@authentication_classes([]) # No token required so it's easy to test
@permission_classes([])
def college_list_api(request):
    if request.method == 'GET':
        colleges = College.objects.all()
        college_data = []
        for college in colleges:
            college_data.append({
                "id": college.id,
                "name": college.name,
                "address": college.address,
                "phone": college.phone
            })
        return Response({"message": "Successfully fetched all colleges", "data": college_data})

    elif request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        new_college = College.objects.create(
            name=data.get('name'),
            address=data.get('address'),
            phone=data.get('phone')
        )
        return Response({"message": "New college created successfully!", "college_id": new_college.id})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def StudentsRegistrations(request):
        import json
        data = json.loads(request.body)

        student_id = data.get("student_id")
        event_id = data.get("event_id")
       
        print(student_id)

      
        required_student = Students.objects.get(id=student_id)
        event_id = Event.objects.get(id=event_id)

        StudentsRegistration.objects.create(
            event= event_id,
            student= required_student,
            registration_date= datetime.now()
        ).save()
        return Response({"message":"Student registered successfully"})


@api_view(['GET','POST','PUT','DELETE'])
def student_detail(request,college_id):
    if request.method == 'GET' or 'POST' or 'PUT' or 'DELETE':
        StudentsRegistration = StudentsRegistration.objects.filter(college_id = college_id)    
        students_list = []
        for i in StudentsRegistrations:
            students_list.append({
            'name':i.student.name,
            'age':i.student.age,
            'email':i.student.email,
            'is_registered':i.is_registered,
            'college':i.college.name,
            'address':i.college.address,
            'phone':i.college.phone,
            'principal':i.college.principal
        })
    print(StudentsRegistrations)
    return Response({"StudentsRegistration":students_list})


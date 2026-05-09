from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Event
import json

@api_view(['GET', 'POST'])
@authentication_classes([]) # No token required
@permission_classes([])
def event_list_api(request):
    if request.method == 'GET':
        events = Event.objects.all()
        event_data = []
        for event in events:
            event_data.append({
                "id": event.id,
                "name": event.name,
                "date": event.date,
                "location": event.location
            })
        return Response({"message": "Successfully fetched all events", "data": event_data})

    elif request.method == 'POST':
        data = json.loads(request.body)
        new_event = Event.objects.create(
            name=data.get('name'),
            date=data.get('date'),
            location=data.get('location')
        )
        return Response({"message": "New event created successfully!", "event_id": new_event.id})

from django.contrib.auth.models import User
from rest_framework import serializers
from Event.models import Event
from Event.models import Eventregistration


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventregistration
        fields = '__all__'      


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
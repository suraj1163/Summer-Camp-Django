from rest_framework import serializers
from .models import user_application, user_application_list

class user_application_serializers(serializers.ModelSerializer):
    class Meta:
        model = user_application
        fields = '__all__'

class user_application_list_serializers(serializers.ModelSerializer):
    class Meta:
        model = user_application_list
        fields = '__all__'
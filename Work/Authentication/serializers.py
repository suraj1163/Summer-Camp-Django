from rest_framework import serializers
from .models import user_register, user_login, user_profile

class user_register_serializers(serializers.ModelSerializer):
    class Meta:
        model = user_register
        fields = '__all__'

class user_login_serializers(serializers.ModelSerializer):
    class Meta:
        model = user_login
        fields = '__all__'

class user_profile_serializers(serializers.ModelSerializer):
    class Meta:
        model = user_profile
        fields = '__all__'
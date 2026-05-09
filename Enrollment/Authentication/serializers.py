from rest_framework import serializers
from .models import UserInfo

class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta: ##shortcut for meta class(database axis)
        model = UserInfo
        fields = ['first_name','last_name','email']

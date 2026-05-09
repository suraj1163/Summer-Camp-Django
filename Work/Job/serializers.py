from rest_framework import serializers
from .models import job_category
from .models import job_create
from .models import job_list

class job_category_serializers(serializers.ModelSerializer):
    class Meta:
        model = job_category
        fields = '__all__'

class job_create_serializers(serializers.ModelSerializer):
    class Meta:
        model = job_create
        fields = '__all__'

class job_list_serializers(serializers.ModelSerializer):
    class Meta:
        model = job_list
        fields = '__all__'
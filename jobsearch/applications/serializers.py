from rest_framework import serializers
from applications.models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    candidate = serializers.ReadOnlyField(source='candidate.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('candidate',)

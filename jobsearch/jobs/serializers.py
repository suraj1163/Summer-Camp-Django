from rest_framework import serializers
from jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.ReadOnlyField(source='posted_by.full_name')

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('posted_by',)

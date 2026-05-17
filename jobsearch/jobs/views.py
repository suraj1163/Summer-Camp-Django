from rest_framework import viewsets, permissions
from jobs.models import Job
from jobs.serializers import JobSerializer
from jobsearch.permissions import IsAdminOrJobCreator, IsPoster

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrJobCreator(), IsPoster()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

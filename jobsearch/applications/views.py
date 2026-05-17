from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from applications.models import Application
from applications.serializers import ApplicationSerializer
from jobsearch.permissions import IsAdminOrJobCreator, IsPoster, IsCandidate

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Application.objects.all()
        if user.role == 'job_creator':
            return Application.objects.filter(job__posted_by=user)
        # Candidates get nothing from GET list/detail
        return Application.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsCandidate()]
        # Only admins or job creators can view/update/list
        return [IsAdminOrJobCreator(), IsPoster()]

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

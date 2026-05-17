from rest_framework import permissions

class IsAdminOrJobCreator(permissions.BasePermission):
    """
    Allows access only to Admins or Job Creators.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'job_creator']

class IsPoster(permissions.BasePermission):
    """
    Allows access only to the user who posted the job.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the object is a job or an application linked to a job
        if hasattr(obj, 'posted_by'):
            return obj.posted_by == request.user
        if hasattr(obj, 'job'):
            return obj.job.posted_by == request.user
        return False

class IsCandidate(permissions.BasePermission):
    """
    Allows access only to candidates.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'candidate'

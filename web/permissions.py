from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)



# TODO create permission class for checking verification of mentor and set access for mentors.


class IsMentorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            if request.user.is_authenticated and request.user.is_mentor:
                return bool((request.user.profile_stud.is_verified) or request.user.is_staff or request.user.is_superuser)
        except: return False
            


class IsMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_mentor and request.user.profile.is_verified:
            return True
        else: return False
        
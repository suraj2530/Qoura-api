from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
class IsAuthor(permissions.BasePermission):
    message = 'Only the author can delete the question'

    def has_object_permission(self, request, view, obj):
        #print(obj.author)
        #print(request.user.id)
        if(view.action == 'delete' and obj.author == request.user):
            return super(IsAuthor, self).has_permission(request, view)
        
        if view.action != 'delete':
            return super(IsAuthor, self).has_permission(request, view)
        
        raise PermissionDenied




# class UNAUTHORIZED(APIException):
#     status_code = 503
#     default_detail = 'Service temporarily unavailable, try again later.'
#     default_code = 'service_unavailable'

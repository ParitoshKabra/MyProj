from django.http.response import HttpResponse, JsonResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Lists, Projects

#check on backend created_by for projects and cards

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_active
        return request.user.is_authenticated
    #error here
    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            if request.user in obj.admins.all() or request.user == obj.created_by:
                return True
            return request.user.is_staff
        else:
            return request.user.is_authenticated
class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_active
        else:
            return request.user.is_superuser
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.is_active
        else:
            return request.user.is_staff

class ListPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active 
    #error
    def has_object_permission(self, request, view, obj):
        if request.user in obj.lists_project.members.all() or request.user == obj.lists_project.created_by or request.user.is_staff or request.user.is_superuser:
            return True
        return False

class CanCommentorViewComments(BasePermission):
    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user is obj.card_comments.cards_list.lists_project.members.all() or request.user == obj.commented_by:
                return True
            return self.check_staff_access(request)
        else:
            if request.user == obj.commented_by:
                print(request.method)
                # print("thsi was checked") #why!
                return True
            return self.check_staff_access(request)
class CardAssignPermissionorAccess(BasePermission):
    message = "Cannot assign card to a user who is not the member of the project"
    
    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser

    def has_permission(self, request, view):
        try:
            if self.check_staff_access(request) == False:
                list_ = Lists.objects.get(id = request.data.get('cards_list'))
                project = list_.lists_project
                lt = [user.id for user in project.members.all()]
                user_id = request.user.id
                assigned_users = request.data.getlist("assigned_to")

                if user_id not in lt:
                    self.message = "You are not a member of project or an admin"
                    raise PermissionDenied(self.message)
                lt.sort()
                assigned_users.sort()
               
                if len(lt) < len(assigned_users):
                    return False
                else:
                    for id in assigned_users:
                        print(id)
                        if not int(id) in lt:
                            raise PermissionDenied(self.message)
            return True
        except Lists.DoesNotExist:
            return True
# IsProjectAdmin .........Admins from members, admin must be a member of project
# how to make creator a compulsory member ..........has_perm, has_object_permissions
class CardPermissions(BasePermission):

    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_active
        else:
            return CardAssignPermissionorAccess().has_permission(request=request, view=view)


# how to give method specific permisssion in a viewset
# pagination in djangorest, modified project only fetched
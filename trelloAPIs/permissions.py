from django.http.response import HttpResponse, JsonResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Lists, Projects


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_active
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            if request.user in obj.members.all():
                return True
            return request.user.is_staff
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
    def has_object_permission(self, request, view, obj):
        if request.user in obj.lists_project.members.all():
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            if request.user in obj.cards_list.list_projects.members.all():
                return True
        else:
            if request.user is obj.created_by:
                return True
        return self.check_staff_access(request)

class CanCommentorViewComments(BasePermission):
    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser
    
    def has_permission(self, request, view):
        return self.check_staff_access(request)
    
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            if request.user is obj.card_comments.cards_list.projects_list.members.all():
                return True
            return self.check_staff_access(request)
        elif request.method != "GET":
            if request.user is obj.commented_by:
                return True
            return self.check_staff_access(request)
        else:
            if request.user is obj.comment_by or request.user is obj.card_comments.cards_list.projects_list.members.all():
                return True
            return self.check_staff_access(request)

class CardAssignPermissionorAccess(BasePermission):
    message = "Cannot assign card to a user who is not the member of the project"
    
    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser

    def has_permission(self, request, view):
        try:
            super().has_permission(request, view)
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
                    print("came in length if")
                    return False
                else:
                    print("came here in else")
                    for id in assigned_users:
                        print(id)
                        if not int(id) in lt:
                            raise PermissionDenied(self.message)
            return True
        except Lists.DoesNotExist:
            return True
# get_permission ,assigned_cards, IsAdminUser Post view on getting a viewset, how to give method specific permisssion in a viewset

class CardPermissions(BasePermission):

    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_active
        else:
            return CardAssignPermissionorAccess().has_permission(request=request, view=view)
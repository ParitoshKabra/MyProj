from django.http.response import HttpResponse, JsonResponse
from rest_framework.permissions import BasePermission
from .models import Lists, Projects


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_active and request.user.is_authenticated
        else:
            if request.user in obj.members.all():
                return True
            return False
class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_authenticated and request.user.is_active
        else:
            return request.user.is_superuser
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.is_active and request.user.is_authenticated
        else:
            return request.user.is_staff or request.user.is_superuser

class ListPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.user in obj.lists_project.members.all():
            return True
        return False

class CardPermissions(BasePermission):

    def check_staff_access(self, request):
        return request.user.is_staff or request.user.is_superuser

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_active and request.user.is_authenticated
        elif request.method == "POST":
            try:
                list_ = Lists.objects.get(id = request.data.get('cards_list'))
                project = list_.list_projects
                # print(project)
                # print(request.data)
                lt = [user.id for user in project.members.all()]
                print(request.data.getlist("assigned_to"))
                for id in request.data.getlist("assigned_to"):
                    for project_ids in lt:
                        if id != project_ids:
                            return False
                return request.is_superuser or request.user.is_staff or request.user in project.members.all()#check for member
            except Exception as e:
                return request.user.is_active and request.user.is_authenticated
        else:
            return False
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            if request.user in obj.cards_list.list_projects.members.all():
                return True
        else:
            if request.user is obj.created_by:
                return True
        return self.check_staff_access(request)
# only card creator/ project-admins should be able to assign cards, what my view should be for it
# any authenticated user should be able to see his assigned cards (normal function based view is okayy)

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

# get_permission, related_name, assigned_cards, IsAdminUser Post view on getting a viewset, how to give method specific permisssion in a viewset
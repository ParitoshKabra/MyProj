from trelloAPIs.models import Comments
from rest_framework import routers

from .views import CardApiViewSet, CommentApiViewSet, ListApiViewSet, ProjectMakeAdminViewSet, ProjectMemberApiViewSet, UserApiViewSet, UserListApiViewSet, ProjectApiViewSet

router = routers.DefaultRouter()
router.register('users_all', UserListApiViewSet)
router.register('user', UserApiViewSet, basename="user")
router.register('projects', ProjectApiViewSet, basename="projects")
router.register('lists', ListApiViewSet)
router.register('cards', CardApiViewSet)
router.register('comments', CommentApiViewSet)
router.register('project_members', ProjectMemberApiViewSet, basename="project_members")
router.register('make_project_admin', ProjectMakeAdminViewSet)
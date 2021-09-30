from trelloAPIs.models import Comments
from rest_framework import routers
from .views import CardApiViewSet, CommentApiViewSet, ListApiViewSet, ProjectMemberApiviewSet, UserApiViewSet, UserListApiViewSet, ProjectApiViewSet

router = routers.DefaultRouter()
router.register('users_all', UserListApiViewSet)
router.register('user', UserApiViewSet, basename="user")
router.register('projects', ProjectApiViewSet)
router.register('lists', ListApiViewSet)
router.register('cards', CardApiViewSet)
router.register('comments', CommentApiViewSet)
router.register('project_members', ProjectMemberApiviewSet, basename="project_members")
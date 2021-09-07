from trelloAPIs.models import Comments
from rest_framework import routers
from .views import CardApiViewSet, CommentApiViewSet, ListApiViewSet, UserApiViewSet, ProjectApiViewSet

router = routers.DefaultRouter()
router.register('users', UserApiViewSet)
router.register('projects', ProjectApiViewSet)
router.register('lists', ListApiViewSet)
router.register('cards', CardApiViewSet)
router.register('comments', CommentApiViewSet)
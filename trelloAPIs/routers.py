from rest_framework import routers
from .views import UserApiViewSet, ProjectApiViewSet

router = routers.DefaultRouter()
router.register('users', UserApiViewSet)
router.register('projects', ProjectApiViewSet)
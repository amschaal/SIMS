from rest_framework import routers
from sims.api.views import ProjectViewSet, SampleViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'samples', SampleViewSet)

urlpatterns = router.urls
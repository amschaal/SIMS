from rest_framework import routers
from sims.api.views import ProjectViewSet, SampleViewSet, PoolViewSet,\
    LibraryViewSet, AdapterViewSet, RunViewSet, MachineViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'pools', PoolViewSet)
router.register(r'libraries', LibraryViewSet)
router.register(r'adapters', AdapterViewSet)
router.register(r'runs', RunViewSet)
router.register(r'machines', MachineViewSet)

urlpatterns = router.urls
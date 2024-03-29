from rest_framework import routers
from djson.api.views import ModelTypeViewset, ContentTypeViewset
from sims.api.views import ProjectViewSet, SampleViewSet, PoolViewSet,\
    LibraryViewSet, AdapterViewSet, RunViewSet, MachineViewSet, RunPoolViewSet,\
    AdapterDBViewset, SubmissionViewSet, SubmissionTypeViewSet

router = routers.SimpleRouter()
router.register(r'submissions', SubmissionViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'pools', PoolViewSet)
router.register(r'libraries', LibraryViewSet)
router.register(r'adapters/(?P<db>[^/.]+)', AdapterViewSet)
router.register(r'adapter_db', AdapterDBViewset)
router.register(r'runs', RunViewSet)
router.register(r'run_pools', RunPoolViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'model_types', ModelTypeViewset)
router.register(r'content_types', ContentTypeViewset)
router.register(r'submission_types', SubmissionTypeViewSet, 'submission_types')
# router.register(r'jsonschema', JSONSchemaViewSet, 'jsonschema')

urlpatterns = router.urls
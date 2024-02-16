from rest_framework.decorators import action
from rest_framework.response import Response
from drf_jsonschema_serializer.convert import to_jsonschema

class JSONSchemaMixin:
    @action(detail=True, methods=['get'])
    def get_schema(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(to_jsonschema(serializer))
class JSONSchemaMixin:
    @action(detail=True, methods=['get'])
    def get_jsonschema(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(to_jsonschema(serializer))
    @action(detail=False, methods=['put','post'])
    def jsonschema(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(to_jsonschema(serializer))
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_jsonschema_serializer.convert import to_jsonschema
from rest_framework import viewsets

# class JSONSchemaMixin:
#     @action(detail=True, methods=['get'])
#     def get_schema(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(to_jsonschema(serializer))
class JSONSchemaMixin:
    @action(detail=True, methods=['get'], url_path='jsonschema', url_name='jsonschema_detail')
    def jsonschema_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(to_jsonschema(serializer))
    @action(detail=False, methods=['put','post', 'get'])
    def jsonschema(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        return Response(to_jsonschema(serializer))

class ActionSerializerMixin:
    """
    Provide the following in model for different serializers
    action_serializers = {
        'retrieve': MyModelDetailSerializer,
        'list': MyModelListSerializer,
        'create': MyModelCreateSerializer
    }
    """
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers.keys():
                return self.action_serializers[self.action]
        return viewsets.ModelViewSet.get_serializer_class(self)
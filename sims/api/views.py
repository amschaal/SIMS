from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from rest_framework.permissions import AllowAny
from sims.api.serializers import UserSerializer

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({'status':'success','user':UserSerializer(instance=user).data})
    else:
        return Response({'message':'Not authenticated.'},status=403)

@api_view(['POST', 'GET'])
def logout_view(request):
    auth_logout(request)
    return Response({'status':'success'})
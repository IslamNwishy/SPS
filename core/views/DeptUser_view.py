from core.models import DeptUser
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.DeptUser_serializer import DeptUserSerializer, DeptUserGetSerializer

class DeptUserView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeptUserSerializer
    get_serializer_class = DeptUserGetSerializer
    model = DeptUser
    
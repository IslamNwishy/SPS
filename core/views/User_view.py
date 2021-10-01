from core.models import User
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.User_serializer import UserSerializer, UserGetSerializer

class UserView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    get_serializer_class = UserGetSerializer
    model = User
    
from core.models import OrderProcess
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.OrderProcess_serializer import OrderProcessSerializer, OrderProcessGetSerializer

class OrderProcessView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProcessSerializer
    get_serializer_class = OrderProcessGetSerializer
    model = OrderProcess
    
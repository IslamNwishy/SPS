from core.models import Order
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Order_serializer import OrderSerializer, OrderGetSerializer

class OrderView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    get_serializer_class = OrderGetSerializer
    model = Order
    
from core.models import Seller
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Seller_serializer import SellerSerializer, SellerGetSerializer

class SellerView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SellerSerializer
    get_serializer_class = SellerGetSerializer
    model = Seller
    
from core.models import Offer
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Offer_serializer import OfferSerializer, OfferGetSerializer

class OfferView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OfferSerializer
    get_serializer_class = OfferGetSerializer
    model = Offer
    
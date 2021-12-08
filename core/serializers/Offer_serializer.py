
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import Offer
    
from core.serializers.Order_serializer import OrderGetSerializer
from core.serializers.Seller_serializer import SellerGetSerializer

class OfferSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = Offer
        fields = "__all__"                        
        
class OfferGetSerializer(DynamicFieldsModelSerializer):
    
    order=OrderGetSerializer()
    seller=SellerGetSerializer()

    class Meta:
        model = Offer
        fields = "__all__"                        
        
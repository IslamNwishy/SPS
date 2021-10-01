
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import Offer
    
from core.serializers.Order_serializer import OrderGetSerializer

class OfferSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = Offer
        fields = "__all__"                        
        
class OfferGetSerializer(DynamicFieldsModelSerializer):
    
    order=OrderGetSerializer()

    class Meta:
        model = Offer
        fields = "__all__"                        
        
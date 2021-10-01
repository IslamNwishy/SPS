
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import Organization
    
from core.serializers.User_serializer import UserGetSerializer

class OrganizationSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = Organization
        fields = "__all__"                        
        
class OrganizationGetSerializer(DynamicFieldsModelSerializer):
    
    admin=UserGetSerializer()

    class Meta:
        model = Organization
        fields = "__all__"                        
        

from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import Document
    
from core.serializers.Organization_serializer import OrganizationGetSerializer

class DocumentSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = Document
        fields = "__all__"                        
        
class DocumentGetSerializer(DynamicFieldsModelSerializer):
    
    org=OrganizationGetSerializer()

    class Meta:
        model = Document
        fields = "__all__"                        
        

from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import Pipeline
    
from core.serializers.Organization_serializer import OrganizationGetSerializer

class PipelineSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = Pipeline
        fields = "__all__"                        
        
class PipelineGetSerializer(DynamicFieldsModelSerializer):
    
    org=OrganizationGetSerializer()

    class Meta:
        model = Pipeline
        fields = "__all__"                        
        
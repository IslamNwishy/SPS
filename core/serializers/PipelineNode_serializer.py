
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import PipelineNode
    
from core.serializers.Pipeline_serializer import PipelineGetSerializer
from core.serializers.Department_serializer import DepartmentGetSerializer
from core.serializers.Document_serializer import DocumentGetSerializer

class PipelineNodeSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = PipelineNode
        fields = "__all__"                        
        
class PipelineNodeGetSerializer(DynamicFieldsModelSerializer):
    
    pipeline=PipelineGetSerializer()
    dept=DepartmentGetSerializer()
    generates_document=DocumentGetSerializer()

    class Meta:
        model = PipelineNode
        fields = "__all__"                        
        
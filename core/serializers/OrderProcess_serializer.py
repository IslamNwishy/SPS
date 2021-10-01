
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import OrderProcess
    
from core.serializers.Order_serializer import OrderGetSerializer
from core.serializers.PipelineNode_serializer import PipelineNodeGetSerializer
from core.serializers.User_serializer import UserGetSerializer

class OrderProcessSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = OrderProcess
        fields = "__all__"                        
        
class OrderProcessGetSerializer(DynamicFieldsModelSerializer):
    
    order=OrderGetSerializer()
    pipeline_node=PipelineNodeGetSerializer()
    checked_by=UserGetSerializer()

    class Meta:
        model = OrderProcess
        fields = "__all__"                        
        

from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import Department
    
from core.serializers.Organization_serializer import OrganizationGetSerializer

class DepartmentSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = Department
        fields = "__all__"                        
        
class DepartmentGetSerializer(DynamicFieldsModelSerializer):
    
    org=OrganizationGetSerializer()

    class Meta:
        model = Department
        fields = "__all__"                        
        
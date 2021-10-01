
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import DeptUser
    
from core.serializers.Department_serializer import DepartmentGetSerializer
from core.serializers.User_serializer import UserGetSerializer

class DeptUserSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = DeptUser
        fields = "__all__"                        
        
class DeptUserGetSerializer(DynamicFieldsModelSerializer):
    
    dept=DepartmentGetSerializer()
    user=UserGetSerializer()

    class Meta:
        model = DeptUser
        fields = "__all__"                        
        
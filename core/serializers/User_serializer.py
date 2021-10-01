
from prototype.serializers import DynamicFieldsModelSerializer
    
from core.models import User
    

class UserSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = User
        fields = "__all__"                        
        
class UserGetSerializer(DynamicFieldsModelSerializer):
    

    class Meta:
        model = User
        fields = "__all__"                        
        
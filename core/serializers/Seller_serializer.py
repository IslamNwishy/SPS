
from prototype.serializers import DynamicFieldsModelSerializer

from core.models import Seller

from core.serializers.User_serializer import UserGetSerializer


class SellerSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Seller
        fields = "__all__"


class SellerGetSerializer(DynamicFieldsModelSerializer):

    user = UserGetSerializer()

    class Meta:
        model = Seller
        fields = "__all__"

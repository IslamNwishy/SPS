
from rest_framework import serializers
from prototype.serializers import DynamicFieldsModelSerializer

from core.models import Order

from core.serializers.Pipeline_serializer import PipelineGetSerializer
from core.serializers.PipelineNode_serializer import PipelineNodeGetSerializer
from core.serializers.Organization_serializer import OrganizationGetSerializer
from core.serializers.User_serializer import UserGetSerializer


class OrderSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class OrderGetSerializer(DynamicFieldsModelSerializer):

    pipeline = PipelineGetSerializer()
    current_node = PipelineNodeGetSerializer()
    org = OrganizationGetSerializer()
    contact_user = UserGetSerializer()
    # chosen_offer=OfferGetSerializer()
    verdict = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_verdict(self, obj):
        types = dict(Order.VERDICT)
        return types[obj.verdict]

from core.models import Order, PipelineNode
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Order_serializer import OrderSerializer, OrderGetSerializer


class OrderView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    get_serializer_class = OrderGetSerializer
    model = Order

    def post(self, request):
        initial_node = PipelineNode.objects.filter(
            pipeline__pk=request.data["pipeline"]).order_by("node_number").first().pk
        request.data.update({
            "contact_user": request.user.pk,
            "org": request.user.dept_user.org.pk,
            "current_node": initial_node,
            "currency": "EGP"
        })
        return super().post(request)

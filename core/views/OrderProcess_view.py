from core.models import OrderProcess
from prototype.views import AutomatorView
from rest_framework import permissions, request
from core.serializers.OrderProcess_serializer import OrderProcessSerializer, OrderProcessGetSerializer


class OrderProcessView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProcessSerializer
    get_serializer_class = OrderProcessGetSerializer
    model = OrderProcess

    def get(self, request, pk=None):
        dept_ = request.user.dept_user.dept
        object = self.model.objects.filter(verdict=OrderProcess.unkown)
        if not dept_:
            return super().get(request, pk, object=object)
        object = object.filter(pipeline_node__dept=dept_)
        return super().get(request, pk=None, object=object)


class OrderProcessHistoryView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProcessSerializer
    get_serializer_class = OrderProcessGetSerializer
    model = OrderProcess
    exclude = ("post", "put", "delete")

    def get(self, request, pk=None):
        dept_ = request.user.dept_user.dept
        object = self.model.objects.filter(
            order__org=request.user.dept_user.org)

        if not dept_:
            return super().get(request, pk, object=object)
        object = object.filter(pipeline_node__dept=dept_)
        return super().get(request, pk=None, object=object)

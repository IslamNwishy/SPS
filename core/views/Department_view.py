from core.models import Department
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Department_serializer import DepartmentSerializer, DepartmentGetSerializer


class DepartmentView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    get_serializer_class = DepartmentGetSerializer
    model = Department

    def get(self, request, pk=None):
        object = self.model.objects.filter(org=request.user.dept_user.org)
        return super().get(request, pk, object)

    def post(self, request):
        request.data.update({
            "org": request.user.dept_user.org.pk
        })
        return super().post(request)

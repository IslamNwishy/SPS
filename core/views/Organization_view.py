from core.models import Organization
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Organization_serializer import OrganizationSerializer, OrganizationGetSerializer

class OrganizationView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrganizationSerializer
    get_serializer_class = OrganizationGetSerializer
    model = Organization
    
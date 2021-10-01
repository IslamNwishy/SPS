from core.models import Pipeline
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Pipeline_serializer import PipelineSerializer, PipelineGetSerializer

class PipelineView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PipelineSerializer
    get_serializer_class = PipelineGetSerializer
    model = Pipeline
    
from core.models import PipelineNode
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.PipelineNode_serializer import PipelineNodeSerializer, PipelineNodeGetSerializer

class PipelineNodeView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PipelineNodeSerializer
    get_serializer_class = PipelineNodeGetSerializer
    model = PipelineNode
    
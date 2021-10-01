from core.models import Document
from prototype.views import AutomatorView
from rest_framework import permissions
from core.serializers.Document_serializer import DocumentSerializer, DocumentGetSerializer

class DocumentView(AutomatorView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    get_serializer_class = DocumentGetSerializer
    model = Document
    
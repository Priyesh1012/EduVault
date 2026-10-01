from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document
from .serializers import DocumentSerializer

from .permissions import IsCommittee
from .serializers import (
    DocumentSerializer,
    CommitteeDocumentSerializer,
    RejectDocumentSerializer,
)

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status=Document.Status.PENDING
        )


class DocumentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()

        if document.status != Document.Status.PENDING:
            return Response(
                {
                    "error": "Only pending documents can be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        document.delete()

        return Response(
            {
                "message": "Document deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class CommitteeDocumentListView(generics.ListAPIView):
    serializer_class = CommitteeDocumentSerializer
    permission_classes = [IsAuthenticated, IsCommittee]

    def get_queryset(self):
        return Document.objects.all().order_by("-created_at")    

class CommitteeVerifyDocumentView(generics.UpdateAPIView):
    serializer_class = CommitteeDocumentSerializer
    permission_classes = [IsAuthenticated, IsCommittee]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Document.objects.all()

    def patch(self, request, *args, **kwargs):
        document = self.get_object()

        if document.status != Document.Status.PENDING:
            return Response(
                {
                    "error": "Only pending documents can be verified."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        document.status = Document.Status.VERIFIED
        document.rejection_reason = None
        document.save()

        return Response(
            CommitteeDocumentSerializer(document).data,
            status=status.HTTP_200_OK
        )    

class CommitteeRejectDocumentView(generics.UpdateAPIView):
    serializer_class = RejectDocumentSerializer
    permission_classes = [IsAuthenticated, IsCommittee]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Document.objects.all()

    def patch(self, request, *args, **kwargs):
        document = self.get_object()

        if document.status != Document.Status.PENDING:
            return Response(
                {
                    "error": "Only pending documents can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RejectDocumentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        document.status = Document.Status.REJECTED
        document.rejection_reason = serializer.validated_data[
            "rejection_reason"
        ]
        document.save()

        return Response(
            CommitteeDocumentSerializer(document).data,
            status=status.HTTP_200_OK
        )    
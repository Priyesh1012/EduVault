from django.urls import path

from .views import (
    CommitteeDocumentListView,
    CommitteeVerifyDocumentView,
    CommitteeRejectDocumentView,
)

urlpatterns = [
    path(
        "documents/",
        CommitteeDocumentListView.as_view(),
        name="committee-document-list"
    ),
    path(
        "documents/<int:pk>/verify/",
        CommitteeVerifyDocumentView.as_view(),
        name="committee-document-verify"
    ),
    path(
        "documents/<int:pk>/reject/",
        CommitteeRejectDocumentView.as_view(),
        name="committee-document-reject"
    ),
]
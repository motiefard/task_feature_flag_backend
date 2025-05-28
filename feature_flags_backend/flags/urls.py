from django.urls import path
from .views import (
    FeatureFlagListCreateView,
    FeatureFlagDetailView,
    FeatureFlagToggleView,
    FeatureFlagAuditLogView,
)

urlpatterns = [
    path('flags/', FeatureFlagListCreateView.as_view(), name='flag-list-create'),
    path('flags/<int:pk>/', FeatureFlagDetailView.as_view(), name='flag-detail'),
    path('flags/<int:pk>/toggle/', FeatureFlagToggleView.as_view(), name='flag-toggle'),
    path('flags/<int:pk>/audit/', FeatureFlagAuditLogView.as_view(), name='flag-audit'),
] 
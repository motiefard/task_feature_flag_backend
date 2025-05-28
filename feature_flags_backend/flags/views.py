from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import FeatureFlag, FlagDependency, AuditLog
from .serializers import FeatureFlagSerializer, AuditLogSerializer
from django.db import transaction

# Create your views here.


class FeatureFlagListCreateView(generics.ListCreateAPIView):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer

    def perform_create(self, serializer):
        flag = serializer.save()
        AuditLog.objects.create(
            flag=flag,
            action='create',
            actor=self.request.data.get('actor', 'system'),
            reason=self.request.data.get('reason', 'Created via API')
        )



class FeatureFlagDetailView(generics.RetrieveAPIView):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer





class FeatureFlagToggleView(APIView):
    def post(self, request, pk):
        flag = get_object_or_404(FeatureFlag, pk=pk)
        enable = request.data.get('enable')
        actor = request.data.get('actor', 'system')
        reason = request.data.get('reason', '')
        if enable is None:
            return Response({'detail': 'Missing enable parameter.'}, status=400)
        with transaction.atomic():
            if enable:
                # Check all dependencies are enabled
                deps = FlagDependency.objects.filter(flag=flag)
                for dep in deps:
                    if not dep.depends_on.enabled:
                        return Response({'detail': f"Dependency '{dep.depends_on.name}' is not enabled."}, status=400)
                flag.enabled = True
                flag.save()
                AuditLog.objects.create(flag=flag, action='toggle_on', actor=actor, reason=reason or 'Enabled via API')
            else:
                # Auto-disable all dependents
                dependents = FlagDependency.objects.filter(depends_on=flag)
                for dep in dependents:
                    dep_flag = dep.flag
                    if dep_flag.enabled:
                        dep_flag.enabled = False
                        dep_flag.save()
                        AuditLog.objects.create(flag=dep_flag, action='auto_disable', actor=actor, reason=f"Auto-disabled because dependency '{flag.name}' was disabled.")
                flag.enabled = False
                flag.save()
                AuditLog.objects.create(flag=flag, action='toggle_off', actor=actor, reason=reason or 'Disabled via API')
        return Response({'id': flag.id, 'enabled': flag.enabled})




class FeatureFlagAuditLogView(generics.ListAPIView):
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        flag_id = self.kwargs['pk']
        return AuditLog.objects.filter(flag_id=flag_id).order_by('-timestamp')

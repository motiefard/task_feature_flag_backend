from django.contrib import admin
from .models import FeatureFlag, FlagDependency, AuditLog

# Register your models here.
admin.site.register(FeatureFlag)
admin.site.register(FlagDependency)
admin.site.register(AuditLog)

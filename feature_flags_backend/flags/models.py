from django.db import models

class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="creator")

    def __str__(self):
        return self.name

class FlagDependency(models.Model):
    flag = models.ForeignKey(FeatureFlag, related_name='dependencies', on_delete=models.CASCADE)
    depends_on = models.ForeignKey(FeatureFlag, related_name='dependents', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('flag', 'depends_on')

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('toggle_on', 'Toggle On'),
        ('toggle_off', 'Toggle Off'),
        ('auto_disable', 'Auto Disable'),
    )
    flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    actor = models.CharField(max_length=100)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

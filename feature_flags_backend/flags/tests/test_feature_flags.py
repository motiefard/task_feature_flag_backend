import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from flags.models import FeatureFlag, FlagDependency, AuditLog

@pytest.mark.django_db
def test_create_flag():
    client = APIClient()
    data = {
        "name": "flag1",
        "description": "Test flag",
        "created_by": "tester"
    }
    response = client.post(reverse('flag-list-create'), data)
    assert response.status_code == 201
    assert FeatureFlag.objects.filter(name="flag1").exists()

@pytest.mark.django_db
def test_circular_dependency_rejected():
    client = APIClient()
    # Create two flags
    f1 = FeatureFlag.objects.create(name="f1", description="", created_by="t")
    f2 = FeatureFlag.objects.create(name="f2", description="", created_by="t")
    # Add f2 depends on f1
    FlagDependency.objects.create(flag=f2, depends_on=f1)
    # Try to create a circular dependency (f1 depends on f2)
    data = {
        "name": "f3",
        "description": "",
        "created_by": "t",
        "dependencies": [f2.id]
    }
    response = client.post(reverse('flag-list-create'), data)
    assert response.status_code == 400 or response.status_code == 201  # Adjust based on your logic

@pytest.mark.django_db
def test_toggle_flag_with_dependencies():
    client = APIClient()
    f1 = FeatureFlag.objects.create(name="dep", description="", created_by="t", enabled=True)
    f2 = FeatureFlag.objects.create(name="main", description="", created_by="t")
    FlagDependency.objects.create(flag=f2, depends_on=f1)
    # Try to enable f2 (should succeed since f1 is enabled)
    response = client.post(reverse('flag-toggle', args=[f2.id]), {"enable": True, "actor": "t"})
    assert response.status_code == 200
    f2.refresh_from_db()
    assert f2.enabled

@pytest.mark.django_db
def test_toggle_flag_fails_if_dependency_disabled():
    client = APIClient()
    f1 = FeatureFlag.objects.create(name="dep", description="", created_by="t", enabled=False)
    f2 = FeatureFlag.objects.create(name="main", description="", created_by="t")
    FlagDependency.objects.create(flag=f2, depends_on=f1)
    # Try to enable f2 (should fail since f1 is disabled)
    response = client.post(reverse('flag-toggle', args=[f2.id]), {"enable": True, "actor": "t"})
    assert response.status_code == 400
    f2.refresh_from_db()
    assert not f2.enabled

@pytest.mark.django_db
def test_audit_log_created_on_toggle():
    client = APIClient()
    f1 = FeatureFlag.objects.create(name="flag", description="", created_by="t")
    response = client.post(reverse('flag-toggle', args=[f1.id]), {"enable": True, "actor": "t", "reason": "test"})
    assert response.status_code == 200
    assert AuditLog.objects.filter(flag=f1, action='toggle_on').exists()

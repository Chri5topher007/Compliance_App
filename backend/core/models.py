from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        AUDITOR = 'AUDITOR', 'Auditor'
        AUDITEE = 'AUDITEE', 'Auditee'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.AUDITEE)
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department_head = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ComplianceDocument(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500) 
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    audit_status = models.CharField(max_length=50, default='Pending Review')
    created_at = models.DateTimeField(auto_now_add=True)

class RiskRegister(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=255)
    threat = models.TextField()
    likelihood = models.IntegerField()
    impact = models.IntegerField()
    risk_score = models.IntegerField()
    mitigation_plan = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='Open')

class AuditSchedule(models.Model):
    audit_title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    venue = models.CharField(max_length=255)
    agenda = models.TextField()
    status = models.CharField(max_length=50, default='Scheduled')

class AuditAttendees(models.Model):
    schedule = models.ForeignKey(AuditSchedule, related_name='attendees', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
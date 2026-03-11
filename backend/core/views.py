import pandas as pd
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import EmailMessage
from django.conf import settings
from icalendar import Calendar, Event
from datetime import datetime
from .models import User, Department, ComplianceDocument, RiskRegister, AuditSchedule, AuditAttendees
from .serializers import (
    UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer,
    DepartmentSerializer, DocumentSerializer, RiskSerializer, AuditScheduleSerializer
)

# --- Auth Views ---
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserProfileView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        return self.request.user

# --- Core Feature Views ---
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = ComplianceDocument.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class RiskDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def upload_register(self, request):
        file_obj = request.FILES.get('file')
        dept_id = request.data.get('department_id')
        if not file_obj or not dept_id:
            return Response({"error": "Missing data"}, status=400)

        try:
            df = pd.read_excel(file_obj)
            risks = []
            for _, row in df.iterrows():
                l = int(row['Likelihood'])
                i = int(row['Impact'])
                risks.append(RiskRegister(
                    department_id=dept_id,
                    asset_name=row['Asset'],
                    threat=row['Threat'],
                    likelihood=l,
                    impact=i,
                    risk_score=l*i,
                    mitigation_plan=row.get('Mitigation', '')
                ))
            
            RiskRegister.objects.bulk_create(risks)
            
            # Return dashboard data
            risks_qs = RiskRegister.objects.filter(department_id=dept_id)
            return Response({
                "total_risks": risks_qs.count(),
                "high_risk": risks_qs.filter(risk_score__gte=15).count(),
                "recent": RiskSerializer(risks_qs.order_by('-id')[:5], many=True).data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AuditSchedulerViewSet(viewsets.ModelViewSet):
    queryset = AuditSchedule.objects.all()
    serializer_class = AuditScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        schedule = AuditSchedule.objects.create(
            audit_title=data['audit_title'],
            department_id=data['department_id'],
            start_datetime=data['start_datetime'],
            end_datetime=data['end_datetime'],
            venue=data.get('venue', 'TBD'),
            agenda=data.get('agenda', '')
        )
        
        # Attendees logic simplified for working demo
        return Response({"status": "Scheduled", "id": schedule.id}, status=201)
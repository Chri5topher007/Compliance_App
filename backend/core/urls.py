from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', RegisterView)
router.register(r'departments', DepartmentViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'audit-schedule', AuditSchedulerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileView.as_view({'get': 'retrieve'}), name='profile'),
    path('risk-upload/', RiskDashboardViewSet.as_view({'post': 'upload_register'}), name='risk-upload'),
]
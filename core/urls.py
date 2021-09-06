from django.urls import path
from core.views import *


app_name = 'core'

urlpatterns = [
    path('', LoginView.as_view(), name='user-login'),
    path('login', LoginView.as_view(), name='user-login'),
    path('home', AdminHomeView.as_view(), name='home'),
    path('user-home', UserHomeView.as_view(), name='user-home'),
    path('user-logout/', UserLogout, name='user-logout'),
    path('user-register/', UserRegistrationView.as_view(), name='user-register'),
    path('attendance-request/', AttendanceRequestView.as_view(), name='attendance-request'),
    path('approve-attendance/<str:user_id>', ApproveAttendanceView.as_view(), name='approve-attendance'),
]

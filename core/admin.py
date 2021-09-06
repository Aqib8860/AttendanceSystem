from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'approved',]
    

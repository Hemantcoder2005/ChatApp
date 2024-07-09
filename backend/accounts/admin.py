from django.contrib import admin
from .models import User  

@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active') 
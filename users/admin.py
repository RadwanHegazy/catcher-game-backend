from django.contrib import admin
from .models import User


class UserPanel (admin.ModelAdmin) : 
    list_display = ['full_name','points']

admin.site.register(User, UserPanel)
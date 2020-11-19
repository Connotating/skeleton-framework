from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.forms import ModelForm
from django.contrib.admin.options import ModelAdmin as RoutedModelAdmin
from .models import *


class TestAdmin(admin.ModelAdmin):
    model = Test
    list_display = ['id', 'name']

admin.site.register(Test, TestAdmin)

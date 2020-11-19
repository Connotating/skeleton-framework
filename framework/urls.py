import os
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include, reverse
from logic import views
from logic.models import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from django_filters.views import FilterView
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url, include
from django.contrib.auth.models import User as auth_User
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User as auth_User

# import django_rq


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'test', views.TestViewSet, basename="test")


urlpatterns = [
    # url(r'^api-token-auth/', views.obtain_auth_token), Not in use.....yet
    # -------path(1. URL NAME, 2. views.py class, 3. arbiratry name used for templates--------------------------
    # -----------------------Testing Views-----------------------------------
    # preview credentials for users
    url(r'^admin/', admin.site.urls),
    url('', include((router.urls, 'troutwood'), namespace='scenarios')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

admin.site.site_header = "Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"
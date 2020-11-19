from rest_framework import routers, serializers, viewsets
from .models import *
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User as auth_User
from rest_framework import mixins, generics, filters
# from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import F, Q, Sum, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin
import json

from .serializers import *


class TestViewSet(viewsets.ModelViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.ListModelMixin):
    # permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'id']
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class ListTest(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class DetailTest(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
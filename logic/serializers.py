from rest_framework import routers, serializers, viewsets
from logic.models import *
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
from rest_framework.renderers import JSONRenderer
import json


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'industry'
        )
        # fields = '__all__'
        model = Test
        depth = 1
        exclude = []


    def create(self, validated_data):
        return Scenario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance





# Example
# https://cheat.readthedocs.io/en/latest/django/drf_serializers.html

# class WrapperSerializer(serializers.ModelSerializer):
#     class Meta:
#         depth = 1
#         fields = ['id', 'thing', 'other']
#         model = Wrapper
#
#     thing = ThingSerializer()
#
#     def create(self, validated_data):
#         thing_data = validated_data.pop('model')
#         thing_serializer = ThingSerializer(data=thing_data)
#         thing_serializer.is_valid(raise_exception=True)
#         validated_data['thing'] = thing_serializer.save()
#         instance = super().create(validated_data)
#         return instance
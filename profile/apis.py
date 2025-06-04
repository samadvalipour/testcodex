from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Profile
from . import services


class ProfileDetailAPI(APIView):
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
        last_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
        bio = serializers.CharField(required=False, allow_blank=True)
        avatar = serializers.URLField(required=False, allow_blank=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ['id', 'user', 'first_name', 'last_name', 'bio', 'avatar']

    @extend_schema(responses=OutputSerializer)
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = self.OutputSerializer(profile)
        return Response(serializer.data)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def put(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = services.update_profile(profile=profile, **serializer.validated_data)
        output_serializer = self.OutputSerializer(profile)
        return Response(output_serializer.data)


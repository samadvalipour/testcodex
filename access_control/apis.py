from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from . import services, selectors
from .permissions import require_permission

User = get_user_model()


class PermissionListCreateAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = services.models.Permission
            fields = ['id', 'codename', 'name']

    class InputSerializer(serializers.Serializer):
        codename = serializers.CharField(max_length=100)
        name = serializers.CharField(max_length=100)

    @extend_schema(responses=OutputSerializer(many=True))
    def get(self, request):
        require_permission(request.user, 'can_view_permission')
        permissions_qs = selectors.list_permissions()
        serializer = self.OutputSerializer(permissions_qs, many=True)
        return Response(serializer.data)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        require_permission(request.user, 'can_add_permission')
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        permission = services.create_permission(**serializer.validated_data)
        output_serializer = self.OutputSerializer(permission)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class PermissionDetailAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = services.models.Permission
            fields = ['id', 'codename', 'name']

    class InputSerializer(serializers.Serializer):
        codename = serializers.CharField(max_length=100, required=False)
        name = serializers.CharField(max_length=100, required=False)

    def get_object(self, pk):
        return services.models.Permission.objects.get(pk=pk)

    @extend_schema(responses=OutputSerializer)
    def get(self, request, pk):
        require_permission(request.user, 'can_view_permission')
        permission = self.get_object(pk)
        serializer = self.OutputSerializer(permission)
        return Response(serializer.data)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def put(self, request, pk):
        require_permission(request.user, 'can_change_permission')
        permission = self.get_object(pk)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        permission = services.update_permission(
            permission=permission,
            **serializer.validated_data,
        )
        output_serializer = self.OutputSerializer(permission)
        return Response(output_serializer.data)

    @extend_schema(responses=None)
    def delete(self, request, pk):
        require_permission(request.user, 'can_delete_permission')
        permission = self.get_object(pk)
        services.delete_permission(permission=permission)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleListCreateAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = services.models.Role
            fields = ['id', 'name']

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)

    @extend_schema(responses=OutputSerializer(many=True))
    def get(self, request):
        require_permission(request.user, 'can_view_role')
        roles = selectors.list_roles()
        serializer = self.OutputSerializer(roles, many=True)
        return Response(serializer.data)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        require_permission(request.user, 'can_add_role')
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = services.create_role(**serializer.validated_data)
        output_serializer = self.OutputSerializer(role)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class RoleDetailAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = services.models.Role
            fields = ['id', 'name']

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100, required=False)

    def get_object(self, pk):
        return services.models.Role.objects.get(pk=pk)

    @extend_schema(responses=OutputSerializer)
    def get(self, request, pk):
        require_permission(request.user, 'can_view_role')
        role = self.get_object(pk)
        serializer = self.OutputSerializer(role)
        return Response(serializer.data)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def put(self, request, pk):
        require_permission(request.user, 'can_change_role')
        role = self.get_object(pk)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = services.update_role(role=role, **serializer.validated_data)
        output_serializer = self.OutputSerializer(role)
        return Response(output_serializer.data)

    @extend_schema(responses=None)
    def delete(self, request, pk):
        require_permission(request.user, 'can_delete_role')
        role = self.get_object(pk)
        services.delete_role(role=role)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignPermissionToRoleAPI(APIView):
    @extend_schema(responses=None)
    def post(self, request, role_id, permission_id):
        require_permission(request.user, 'can_assign_permission_to_role')
        role = services.models.Role.objects.get(pk=role_id)
        permission = services.models.Permission.objects.get(pk=permission_id)
        services.assign_permission_to_role(role=role, permission=permission)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemovePermissionFromRoleAPI(APIView):
    @extend_schema(responses=None)
    def post(self, request, role_id, permission_id):
        require_permission(request.user, 'can_remove_permission_from_role')
        role = services.models.Role.objects.get(pk=role_id)
        permission = services.models.Permission.objects.get(pk=permission_id)
        services.remove_permission_from_role(role=role, permission=permission)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignRoleToUserAPI(APIView):
    @extend_schema(responses=None)
    def post(self, request, user_id, role_id):
        require_permission(request.user, 'can_assign_role_to_user')
        user = User.objects.get(pk=user_id)
        role = services.models.Role.objects.get(pk=role_id)
        services.assign_role_to_user(role=role, user=user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveRoleFromUserAPI(APIView):
    @extend_schema(responses=None)
    def post(self, request, user_id, role_id):
        require_permission(request.user, 'can_remove_role_from_user')
        user = User.objects.get(pk=user_id)
        role = services.models.Role.objects.get(pk=role_id)
        services.remove_role_from_user(role=role, user=user)
        return Response(status=status.HTTP_204_NO_CONTENT)


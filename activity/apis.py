from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from actstream.models import Action

from access_control.permissions import require_permission
from . import services, selectors, models

User = get_user_model()


class ActivityTargetListAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.ActivityTarget
            fields = ['id', 'title']

    def get(self, request):
        require_permission(request.user, 'can_view_activity_target')
        targets = selectors.list_activity_targets()
        serializer = self.OutputSerializer(targets, many=True)
        return Response(serializer.data)


class FollowTargetForUserAPI(APIView):
    def post(self, request, user_id, target_id):
        require_permission(request.user, 'can_assign_target_to_user')
        user = User.objects.get(pk=user_id)
        target = models.ActivityTarget.objects.get(pk=target_id)
        services.follow_target(user=user, target=target)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnfollowTargetForUserAPI(APIView):
    def post(self, request, user_id, target_id):
        require_permission(request.user, 'can_remove_target_from_user')
        user = User.objects.get(pk=user_id)
        target = models.ActivityTarget.objects.get(pk=target_id)
        services.unfollow_target(user=user, target=target)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollowedTargetsAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.ActivityTarget
            fields = ['id', 'title']

    def get(self, request, user_id):
        require_permission(request.user, 'can_view_activity_target')
        user = User.objects.get(pk=user_id)
        targets = selectors.list_followed_targets_for_user(user=user)
        serializer = self.OutputSerializer(targets, many=True)
        return Response(serializer.data)




class UnseenActivitiesCountAPI(APIView):
    def get(self, request):
        require_permission(request.user, 'can_view_activity')
        count = services.get_unseen_activities_count(user=request.user)
        return Response({'count': count})


class UnseenActivitiesAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Action
            fields = [
                'id',
                'verb',
                'actor_content_type',
                'actor_object_id',
                'target_content_type',
                'target_object_id',
                'timestamp',
            ]

    def get(self, request, target_id):
        require_permission(request.user, 'can_view_activity')
        target = models.ActivityTarget.objects.get(pk=target_id)
        actions = selectors.list_unseen_activities(user=request.user, target=target)
        serializer = self.OutputSerializer(actions, many=True)
        return Response(serializer.data)


class SeenActivitiesAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Action
            fields = [
                'id',
                'verb',
                'actor_content_type',
                'actor_object_id',
                'target_content_type',
                'target_object_id',
                'timestamp',
            ]

    def get(self, request, target_id):
        require_permission(request.user, 'can_view_activity')
        target = models.ActivityTarget.objects.get(pk=target_id)
        actions = selectors.list_seen_activities(user=request.user, target=target)
        serializer = self.OutputSerializer(actions, many=True)
        return Response(serializer.data)


class ObjectActivitiesAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Action
            fields = [
                'id',
                'verb',
                'actor_content_type',
                'actor_object_id',
                'target_content_type',
                'target_object_id',
                'timestamp',
            ]

    def get(self, request, content_type_id, object_id):
        require_permission(request.user, 'can_view_activity')
        content_type = ContentType.objects.get(pk=content_type_id)
        model_class = content_type.model_class()
        obj = model_class.objects.get(pk=object_id)
        actions = selectors.list_object_activities(obj=obj)
        serializer = self.OutputSerializer(actions, many=True)
        return Response(serializer.data)


class UserActivitiesAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Action
            fields = [
                'id',
                'verb',
                'actor_content_type',
                'actor_object_id',
                'target_content_type',
                'target_object_id',
                'timestamp',
            ]

    def get(self, request, user_id):
        require_permission(request.user, 'can_view_activity')
        user = User.objects.get(pk=user_id)
        actions = selectors.list_user_activities(user=user)
        serializer = self.OutputSerializer(actions, many=True)
        return Response(serializer.data)



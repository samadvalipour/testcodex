"""config URL Configuration"""

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from profile.apis import ProfileDetailAPI
from access_control import apis as ac_views
from otp.apis import OtpAuthAPI
from activity import apis as activity_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('profiles/<int:pk>/', ProfileDetailAPI.as_view()),
    path('access-control/permissions/', ac_views.PermissionListCreateAPI.as_view()),
    path('access-control/permissions/<int:pk>/', ac_views.PermissionDetailAPI.as_view()),
    path('access-control/roles/', ac_views.RoleListCreateAPI.as_view()),
    path('access-control/roles/<int:pk>/', ac_views.RoleDetailAPI.as_view()),
    path('access-control/roles/<int:role_id>/permissions/<int:permission_id>/assign/', ac_views.AssignPermissionToRoleAPI.as_view()),
    path('access-control/roles/<int:role_id>/permissions/<int:permission_id>/remove/', ac_views.RemovePermissionFromRoleAPI.as_view()),
    path('access-control/users/<int:user_id>/roles/<int:role_id>/assign/', ac_views.AssignRoleToUserAPI.as_view()),
    path('access-control/users/<int:user_id>/roles/<int:role_id>/remove/', ac_views.RemoveRoleFromUserAPI.as_view()),
    path('otp/', OtpAuthAPI.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activity/targets/', activity_views.ActivityTargetListAPI.as_view()),
    path('activity/users/<int:user_id>/targets/<int:target_id>/follow/', activity_views.FollowTargetForUserAPI.as_view()),
    path('activity/users/<int:user_id>/targets/<int:target_id>/unfollow/', activity_views.UnfollowTargetForUserAPI.as_view()),
    path('activity/users/<int:user_id>/targets/', activity_views.UserFollowedTargetsAPI.as_view()),
    path('activity/unseen-count/', activity_views.UnseenActivitiesCountAPI.as_view()),
    path('activity/targets/<int:target_id>/unseen/', activity_views.UnseenActivitiesAPI.as_view()),
    path('activity/targets/<int:target_id>/seen/', activity_views.SeenActivitiesAPI.as_view()),
    path('activity/objects/<int:content_type_id>/<int:object_id>/activities/', activity_views.ObjectActivitiesAPI.as_view()),
    path('activity/users/<int:user_id>/activities/', activity_views.UserActivitiesAPI.as_view()),
]

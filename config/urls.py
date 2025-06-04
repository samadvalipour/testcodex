"""config URL Configuration"""

from django.contrib import admin
from django.urls import path

from profile.apis import ProfileDetailAPI
from access_control import apis as ac_views
from otp.apis import OtpAuthAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
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
]

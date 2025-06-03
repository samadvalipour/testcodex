"""config URL Configuration"""

from django.contrib import admin
from django.urls import path

from profile.apis import ProfileDetailAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/<int:pk>/', ProfileDetailAPI.as_view()),
]

from django.contrib import admin

from .models import ActivityTargets, ActivitySeenStatus

admin.site.register(ActivityTargets)
admin.site.register(ActivitySeenStatus)

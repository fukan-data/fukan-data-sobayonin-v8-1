from django.contrib import admin

from scheduler.models.task import Task

admin.site.register(Task)

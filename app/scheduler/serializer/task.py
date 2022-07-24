# coding: utf-8

from rest_framework import serializers

from scheduler.models.task import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'mail')

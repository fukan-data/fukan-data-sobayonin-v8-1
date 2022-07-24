from common.models.common_columns import CommonColumns
from django.db import models
from scheduler.models.task import Task


class TaskOption(CommonColumns):
    """スケジューラーのタスクのオプションデータ"""

    class Meta:
        db_table = 'task_option'

    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL, related_name='task')
    url = models.CharField(verbose_name='url', max_length=256, null=True, blank=True)

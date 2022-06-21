from common.models.common_columns import CommonColumns
from django.db import models
from scheduler.enums.task_status import TaskStatus
from scheduler.enums.task_category import TaskCategory


class Task(CommonColumns):
    """スケジューラーのタスクキュー"""

    class Meta:
        db_table = 'task'

    task_id = models.AutoField(verbose_name='タスクID', primary_key=True, blank=True)
    task_service = models.CharField(verbose_name='タスクサービス名', max_length=16)
    # task_service_id = models.IntegerField(verbose_name='タスクサービスID')
    task_name = models.CharField(verbose_name='タスク名', max_length=64)
    task_category = models.IntegerField(verbose_name='タスクカテゴリー', choices=TaskCategory.choices())
    task_status = models.IntegerField(verbose_name='タスクステータス', choices=TaskStatus.choices())
    reserve_start = models.DateTimeField(verbose_name='予約開始日時', null=True, blank=True)
    run_start = models.DateTimeField(verbose_name='実行開始日時', null=True, blank=True)
    run_end = models.DateTimeField(verbose_name='実行終了日時', null=True, blank=True)
    max_time = models.IntegerField(verbose_name='実行最大時間（分）', null=True, blank=True)
    notification_emails = models.CharField(verbose_name='通知メール先', max_length=256, null=True, blank=True)
    notification_slack_url = models.CharField(verbose_name='通知スラック先', max_length=128, null=True, blank=True)
    task_message = models.CharField(verbose_name='タスクメッセージ', max_length=256, null=True, blank=True)

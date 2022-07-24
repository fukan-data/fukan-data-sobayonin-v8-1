from django import forms

from common.forms.common_form import CommonForm
from scheduler.enums.task_category import TaskCategory
from scheduler.enums.task_status import TaskStatus


# BaseFormを継承する
class IndexForm(CommonForm):
    task_service = forms.CharField(
        label='タスクサービス名',
        required=True,
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'task__service-name'}),
    )
    task_service_id = forms.IntegerField(
        label='タスクサービスID',
        required=True,
        min_value=0,
        widget=forms.TextInput(attrs={'class': 'task__service-id'}),
    )
    task_name = forms.CharField(
        label='タスク名',
        required=True,
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'task__task-name'}),
    )
    task_category = forms.TypedChoiceField(
        label='タスクカテゴリー',
        required=True,
        choices=TaskCategory.choices(),
        coerce=int,
        widget=forms.TextInput(attrs={'class': 'task__task-category'}),
    )
    task_status = forms.TypedChoiceField(
        label='タスクステータス',
        required=True,
        choices=TaskStatus.choices(),
        coerce=int,
        widget=forms.TextInput(attrs={'class': 'task__task-status'}),
    )
    reserve_start = forms.DateTimeField(
        label='予約開始日時',
        widget=forms.TextInput(attrs={'class': 'task__reserve-start'}),
    )
    max_time = forms.IntegerField(
        label='実行最大時間（分）',
        required=True,
        min_value=0,
        widget=forms.TextInput(attrs={'class': 'task__max-time'}),
    )
    notification_emails = forms.CharField(
        label='通知メール先',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'task__notification-emails'}),
    )
    notification_slack_url = forms.CharField(
        label='通知スラック先',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'task__notification-slack-url'}),
    )

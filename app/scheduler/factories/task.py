from scheduler.models import Task
from faker import Faker
from factory.django import DjangoModelFactory
from scheduler.enums.task_category import TaskCategory
from scheduler.enums.task_status import TaskStatus
from django.utils import timezone

fakegen = Faker("ja_JP")


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task
    task_service = 'sns'
    task_name = 'facebook_announcement'
    task_category = TaskCategory.SINGLE.no
    task_status = TaskStatus.WAITING.no
    max_time = 20
    reserve_start = timezone.localtime()
    notification_emails = 'fukan.data.labo@gmail.com'
    notification_slack_url = 'https://hooks.slack.com/services/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'

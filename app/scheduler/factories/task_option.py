from scheduler.models import TaskOption
from faker import Faker
from factory.django import DjangoModelFactory

fakegen = Faker("ja_JP")


class TaskOptionFactory(DjangoModelFactory):
    class Meta:
        model = TaskOption
    task_id = 1
    url = 'https://hooks.slack.com/services/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'

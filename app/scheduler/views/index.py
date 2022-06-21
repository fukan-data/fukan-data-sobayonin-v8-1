from django.views.generic import ListView, TemplateView

from scheduler.models import Task
from scheduler.services.task import TaskService
from scheduler.forms.index import IndexForm
from scheduler.enums.task_status import TaskStatus

import logging

logger = logging.getLogger("django")


class IndexView(ListView):
    template_name = 'index.html'
    model = Task

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.service = TaskService()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['aaa'] = 'hihihihi1234'
        # ctx['form'] = IndexForm()

        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        return ctx

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) # Article.objects.all() と同じ結果

        # GETリクエストパラメータにkeywordがあれば、それでフィルタする
        task_services = self.request.GET.get('task_service')
        print(task_services)
        if task_services is not None:
            queryset = queryset.filter(task_service__in=task_services)

        # is_publishedがTrueのものに絞り、titleをキーに並び変える
        queryset = queryset.filter(task_status=TaskStatus.WAITING.no).order_by('-reserve_start')
        print(queryset)

        return queryset

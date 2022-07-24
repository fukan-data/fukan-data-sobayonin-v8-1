import datetime
from django.db.models import Q
from django.utils import timezone
# import logging
# import logging.handlers
# from django.db import transaction

from common.services.common_service import CommonService
from common.services.selenium_service import SeleniumService
from common.services.google.spread_sheet_service import SpreadSheetService
from common.enums.status import Status
from scheduler.models.task_option import TaskOption
from scheduler.enums.task_status import TaskStatus


class TaskService(CommonService):
    def __init__(self, logger=None, **kwargs):
        self.logger = self.get_logger(filename='task.log') if logger is None else logger
        super().__init__(**kwargs)
        self.TASK_QUEUE_SSID = '1sHRAjR3x4QrMgPS_SSNmTW0WF0qpKFkUHsCfaSY02qU'
        self.TASK_QUEUE_SHEET_NAME = 'queue'
        self.spread_sheet_service = SpreadSheetService(self.logger)








    # def get_logger(self, is_rotate=True):
    #     log_service = LogService()
    #     return log_service.get_logger(filename="task.log", is_rotate=is_rotate)

    def is_working_time(self, start_h, start_m, end_h, end_m):
        tzinfo = self.get_timezone()
        now = datetime.datetime.now(tzinfo)
        now_y = now.year
        now_m = now.month
        now_d = now.day
        input_start = datetime.datetime(now_y, now_m, now_d, start_h, start_m, 0, tzinfo=tzinfo)
        input_end = datetime.datetime(now_y, now_m, now_d, end_h, end_m, 0, tzinfo=tzinfo)
        # 24:00を挟まない場合
        if start_h <= end_h:
            if input_start <= now and now <= input_end:
                return False
        else:
            # 24:00を挟む場合
            absolute_start = datetime.datetime(now_y, now_m, now_d, 0, 0, 0, tzinfo=tzinfo)
            absolute_end = datetime.datetime(now_y, now_m, now_d, 23, 59, 59, tzinfo=tzinfo)
            if (absolute_start <= now and now <= input_end) or (input_start <= now and now <= absolute_end):
                return False
        return True

    def get_tasks(self):
        return TaskOption.objects.select_related('task').filter(
            Q(task__task_status__in=[TaskStatus.WAITING.no, TaskStatus.RUNNING.no]),
            Q(task__reserve_start__lte=timezone.localtime()) | Q(task__reserve_start=None)
        ).all()

    def regist_task_sheet(self, task):
        # append_row

        row = [
            task.task.task_id, task.task.task_service, task.task.task_name, task.task.task_category,
            task.task.task_status, task.url, 'task.task.reserve_star', '', '', '', task.task.max_time,
            task.task.notification_emails, task.task.notification_slack_url, ''
        ]

        print(row)

        self.spread_sheet_service.append_row(self.TASK_QUEUE_SSID, self.TASK_QUEUE_SHEET_NAME, row)

        # df_table = self.spread_sheet_service.get_df_table(self.TASK_QUEUE_SSID, self.TASK_QUEUE_SHEET_NAME)
        # df_table.append({
        #     'task_id': task.task.task_id,
        #     'task_service': task.task.task_service,
        #     'task_name': task.task.task_name,
        #     'task_category': task.task.task_category,
        #     'task_status': task.task.task_status,
        #     'url': task.url,
        #     'reserve_start_task': task.task.reserve_start,
        #     'reserve_start_sheet': '',  # datetime.datetime.now(),  #
        #     'run_start': '',
        #     'run_end': '',
        #     'max_time': task.task.max_time,
        #     'notification_emails': task.task.notification_emails,
        #     'notification_slack_url': task.task.notification_slack_url,
        #     'task_message': ''
        # })










        # spread_sheet_service = SpreadSheetService(self.logger)
        # sheet_id = '1sHRAjR3x4QrMgPS_SSNmTW0WF0qpKFkUHsCfaSY02qU'
        # sheet_name = 'bbbb'
        # df_table = spread_sheet_service.get_df_table(sheet_id, sheet_name, columns=['a', 'b', 'c'], where='a=="test"')
        # print(df_table.table)



        return

        sheet_id = '1sHRAjR3x4QrMgPS_SSNmTW0WF0qpKFkUHsCfaSY02qU'
        sheet_name = 'bbbb'
        range_a1 = 'A1:D3'
        response = spread_sheet_service.get_values(sheet_id, sheet_name, range_a1)
        if response.status != Status.SUCCESS.no:
            print(777, 1)

        sheet_id = '1sHRAjR3x4QrMgPS_SSNmTW0WF0qpKFkUHsCfaSY02qU'
        sheet_name = 'bbbb'
        range_a1 = 'A3:D4'
        values = [[1,2,3,4],[10,20,30,40]]
        response = spread_sheet_service.set_values(sheet_id, sheet_name, range_a1, values)
        if response.status != Status.SUCCESS.no:
            print(777, 2)




        pass

    def test(self):
        seleniumService = SeleniumService()
        seleniumService.test()

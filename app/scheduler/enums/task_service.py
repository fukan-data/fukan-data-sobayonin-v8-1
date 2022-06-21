from common.enums.base_enums import BaseEnum
from scheduler.enums.task_queue_type import TaskQueueType


class TaskService(BaseEnum):
    RUN_GAS = (0, 'GASを実行する', TaskQueueType.TASK_SHEET.no)
    CALENDAR_TO_QUEUE = (1, 'カレンダーからキューの取り込み', TaskQueueType.TASK_SHEET.no)

    def __init__(self, no, ja, queue_type):
        self.no = no
        self.ja = ja
        self.queue_type = queue_type

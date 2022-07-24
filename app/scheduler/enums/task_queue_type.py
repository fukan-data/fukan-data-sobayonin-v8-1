from common.enums.base_enums import BaseEnum


class TaskQueueType(BaseEnum):
    TASK_TABLE = (0, 'タスクテーブル', 'task_table')
    TASK_SHEET = (1, 'タスクシート', 'task_sheet')

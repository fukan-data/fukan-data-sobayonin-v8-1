from common.enums.base_enum import BaseEnum


class TaskCategory(BaseEnum):
    SINGLE = (0, '単発実行', 'single execution')
    SCHEDULED = (1, '予定実行', 'scheduled execution')

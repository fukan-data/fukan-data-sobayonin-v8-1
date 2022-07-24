from common.enums.base_enum import BaseEnum


class TaskStatus(BaseEnum):
    WAITING = (0, '待機中', 'waiting')
    RUNNING = (1, '実行中', 'running')
    FINISHED = (2, '完了', 'finished')
    ERROR = (3, 'エラー', 'error')
    TEST = (9, 'テスト', 'test')

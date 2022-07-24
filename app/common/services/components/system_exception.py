# try-exceptにて、特別なエラーを発生させるときに利用
class SystemException(Exception):
    def __init__(self, status=None, status_id=None, message="", data=None, tries=0, delay=1):
        if status is None and status_id is None:
            raise Exception('statusとstatus_idのどちらかを指定してください。')

        if status_id is None:
            status = status.get_status(status_id)

        if data is None:
            data = {}

        self.status = status
        self.message = message
        self.data = data
        self.tries = tries
        self.delay = delay

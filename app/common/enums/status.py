from common.enums.base_enum import BaseEnum
from common.services.components.response import Response


class Status(BaseEnum):
    NOT_DETECT = (0, '未検出', 'Not detected')
    SUCCESS = (200, '成功', 'Success')
    BAD_REQUEST = (400, 'リクエストの不正', 'Bad Request')
    UNAUTHORIZED = (401, '認証の失敗', 'Unauthorized')
    FORBIDDEN = (403, 'リクエスト先のアクセス権がない', 'Forbidden')
    NOT_FOUND = (404, 'リクエスト先のページが存在しない', 'Not Found')
    REQUEST_TIMEOUT = (408, 'リクエストの時間切れ', 'Request Timeout')
    FAIL_TO_LOGIN = (408, 'ログイン失敗', 'Fail to login')
    INTERNAL_SERVER_ERROR = (500, 'サーバーエラー', 'Internal Server Error')
    BAD_GATEWAY = (502, 'ゲートウェイがリクエストを拒否', 'Bad Gateway')
    SERVICE_UNAVAILABLE = (503, 'サーバーが一時的に利用できない', 'Service Unavailable')
    GATEWAY_TIMEOUT = (504, '制限時間内にリクエストを処理できない', 'Gateway Timeout')
    GOOGLE_SPREAD_SHEET_ERROR = (520, 'googleのスプレッドシートに関するエラー', 'Google spreadsheet error')
    BIG_QUERY_ERROR = (521, 'big queryの実行に失敗', 'Big query error')

    @staticmethod
    def get_status(status_id):
        for member in Status:
            if member.no == status_id:
                return member
        return NotImplemented

    @staticmethod
    def get_response(status, data=None, detail=''):
        return Response(status=status.no, message=status.en, detail=detail, data=data)

from common.consts.base import BASE
import environ
env = environ.Env()


class FC2:
    class URL:
        BASE_URL = 'https://live.fc2.com/'
        LOGIN_URL = 'https://fc2.com/login.php?ref=livechat'
        LOGIN_AFTER_URL = 'https://live.fc2.com/'
        PERFORMER_SEARCH = 'https://live.fc2.com/manage/performer_search/'

    # class PATH:
    #     class DIR:
    #         STOCK = BASE.PATH.FILE_PATH_STOCK
    #
    #     class FILE:
    #         pass

    class ACCOUNT:
        class CONNECTFAM:
            USER_NAME = 'narijoy1229@gmail.com'
            PASSWORD = env('FC2_PASSWORD_1')

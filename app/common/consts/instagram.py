from common.consts.base import BASE
import environ
env = environ.Env()


class INSTAGRAM:
    class URL:
        BASE_URL = 'https://www.instagram.com/'
        LOGIN_URL = 'https://www.instagram.com/accounts/login/'
        LOGIN_AFTER_URL = 'https://www.instagram.com/accounts/onetap/'

    class PATH:
        class DIR:
            STOCK = BASE.PATH.FILE_PATH_STOCK

        class FILE:
            pass

    class ACCOUNT:
        class CONNECTFAM:
            USER_NAME = 'fukan.data.labo@gmail.com'
            PASSWORD = env('INSTAGRAM_PASSWORD_1')

from time import sleep

from common.enums.status import Status
from common.services.components.system_exception import SystemException


def retry(delay=1, tries=3, close_driver=None):
    def _retry(func):
        def wrapper(*args, **kwargs):
            retry_count = 0
            retry_max = tries
            retry_delay = delay  # エラー時に1sの待機
            response = None

            while retry_count < retry_max:
                try:
                    data = func(*args, **kwargs)
                    response = Status.get_response(status=Status.SUCCESS, data=data)
                    retry_max = 0

                except SystemException as se:
                    retry_max = se.tries
                    retry_delay = se.delay
                    response = Status.get_response(status=se.status, detail=se.message, data=se.data)

                except Exception as e:
                    response = Status.get_response(status=Status.INTERNAL_SERVER_ERROR, detail=e.__str__())

                finally:
                    retry_count += 1
                    sleep(retry_delay)

                    # 特別条件による全体処理
                    for arg in args:
                        # driverと判定できたとき、closeする
                        if close_driver is not None and 'WebDriver' in str(type(arg)):
                            driver = arg
                            for i, window_handle in reversed(list(enumerate(driver.window_handles))):
                                if i >= close_driver:
                                    driver.switch_to.window(window_handle)
                                    driver.close()

            return response
        return wrapper
    return _retry

from common.enums.status import Status

from common.services.components.system_exception import SystemException
from common.services.selenium_service import SeleniumService
from common.services.site.instagram_service import InstagramService

from scheduler.services.task_service import TaskService

from django.core.management.base import BaseCommand
from google.cloud import bigquery
from google.oauth2 import service_account




# key_path = "common/keys/sobayonin-db-5afdf912e5c7.json"
#
# credentials = service_account.Credentials.from_service_account_file(
#     key_path, scopes=[
#         "https://www.googleapis.com/auth/cloud-platform",
#         "https://www.googleapis.com/auth/drive",
#         "https://www.googleapis.com/auth/bigquery",
#     ],
# )

service = InstagramService()
logger = service.logger


class Command(BaseCommand):
    help = 'Task runner'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--develop', action='store_true')

    def handle(self, *args, **options):
        # logger.info('Start: Task runner')
        print('Start: Task runner')

        driver = None

        if options['develop']:
            # logger.info('Develop mode')
            print('Develop mode')

        try:
            file_name = 'DSC_5373-1.jpg'

            message = """CONNECTFAMでは、ポートレート撮影を随時行なっています📸🥼👗
            普段、フリーで被写体活動をされているモデルさんはもちろん、初心者の方も大歓迎です🔰😎
            お気軽にDMください📨

            ◽️男性15〜29歳
            ◽️女性15〜35歳
            ◽️撮影場所　渋谷、表参道

            ※撮影データは無料で差し上げます🎞️💿

            #connectfam#model#modeling
            #ポートレート#私服撮影#モデル#モデル募集#ポートレートモデル募集#撮影#撮影モデル#被写体#被写体モデル#東京#渋谷#有名になりたい#モデル志望"""

            print('**********************')

            # service.selemium.shut_down_chrome()
            # driver = service.selemium.get_driver()
            #
            # # ログイン
            # login_response = service.login(driver)
            # if login_response.status != Status.SUCCESS.no:
            #     raise SystemException(status_id=login_response.status)

            # page_name = 'connectfam9'
            # service.read_page(driver, page_name)

            # max_count = 30
            # key_word = '社長'
            # select_hash_list = ['起業家', 'フリーランス', '経営者', '男', '変態', 'AV']
            # service.search_tag(driver, key_word, select_hash_list, max_count)

            max_count = 1000
            key_word = 'カメラマンさんと繋がりたい'  # 女子会
            page_name = 'takuhai3063'
            select_hash_list = []
            # service.search_tag(driver, key_word, select_hash_list, max_count)
            # service.search_tag_direct(page_name, key_word, select_hash_list, max_count)
            service.search_tag_dev_mode(page_name, key_word, select_hash_list, max_count)


            service.search_tag_android_mode(page_name, key_word, select_hash_list, max_count)




            # page_name = 'connectfam9'
            # service.search_followers(driver, page_name)









# グラビアアイドル



            return

            service.throw(3, file_name, message)



        except SystemException as se:
            logger.error(se.__str__())
            if driver is not None:
                driver.close()

        except Exception as e:
            logger.error(e.__str__())
            if driver is not None:
                driver.close()


        exit(0)



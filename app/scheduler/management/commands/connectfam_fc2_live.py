from common.enums.status import Status

from common.services.components.system_exception import SystemException
from common.services.site.fc2_service import Fc2Service

from django.core.management.base import BaseCommand


service = Fc2Service()
logger = service.logger


class Command(BaseCommand):
    help = 'Task runner'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--develop', action='store_true')

    def handle(self, *args, **options):
        # logger.info('Start: Task runner')
        print('Start: Task runner')
        print('**********************')

        driver = None

        if options['develop']:
            # logger.info('Develop mode')
            print('Develop mode')

        try:
            driver = service.selemium.get_driver()

            # ログイン
            login_response = service.login(driver)
            if login_response.status != Status.SUCCESS.no:
                raise SystemException(status_id=login_response.status, message=login_response.detail)

            # パフォーマー一覧情報の取得
            update_performer_response = service.search_performers(driver)
            if update_performer_response.status != Status.SUCCESS.no:
                raise SystemException(status_id=update_performer_response.status, message=update_performer_response.detail)

            for key in update_performer_response.data:
                # パフォーマーの基本情報を更新
                service.search_performer_basic(driver, update_performer_response.data[key])

                # パフォーマーのポイントを更新
                service.search_performer_point(driver, update_performer_response.data[key])

            # パフォーマーのデータを保存
            service.set_performer_info(update_performer_response.data)

            print(update_performer_response.data)


            # # パフォーマーのデータを保存
            # aaa = {'84909097': {'id': '84909097', 'points_sheet_name': '20220801', 'name_sei': '清水', 'name_mei': '柚香', 'nick_name': 'ふうか', 'belong': 'JOY LLC', 'favorite_by': '242', 'point': '61365', 'personal_url': 'https://live.fc2.com/manage/performer_edit/?cid=38488828', 'point_url': 'https://live.fc2.com/manage/monthly/?managerId=38316275&castId=38488828', 'email': 'mt90zig8em89ie@live.fc2.com', 'login_id': 'ig8em89ie', 'login_password': 'qY9bZ0uU', 'name': '姓： 名：', 'name_kana': 'セイ: メイ:', 'name_kana_sei': 'シミズ', 'name_kana_mei': 'ユウカ', 'birth_day': '2000/11/22', 'contact': '', 'identification': '身分証明書追加登録', 'country_place': '配信除外国・地域指定', 'reward_ratio': '35', 'stop_type': '何もしない 12時間 24時間', 'points_sum': '61,365 pt. (50,718 pt.)', 'points': [['2022/08/01', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/02', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/03', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/04', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/05', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/06', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/07', '0 pt. (0 pt.)', '14,910 pt. (12,323 pt.)', '14,910 pt. (12,323 pt.)'], ['2022/08/08', '0 pt. (0 pt.)', '46,455 pt. (38,395 pt.)', '46,455 pt. (38,395 pt.)'], ['2022/08/09', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/10', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/11', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/12', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0pt. (0 pt.)'], ['2022/08/13', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/14', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/15', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/16', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/17', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/18', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/19', '0 pt. (0 pt.)', '0 pt.(0 pt.)', '0 pt. (0 pt.)'], ['2022/08/20', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/21', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/22', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/23', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/24', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/25', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/26', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/27', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/28', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/29', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/30', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)'], ['2022/08/31', '0 pt. (0 pt.)', '0 pt. (0 pt.)', '0 pt. (0 pt.)']]}}
            # service.set_performer_info(aaa)






# グラビアアイドル



            return



        except SystemException as se:
            logger.error(se.__str__())
            if driver is not None:
                driver.close()

        except Exception as e:
            logger.error(e.__str__())
            if driver is not None:
                driver.close()


        exit(0)



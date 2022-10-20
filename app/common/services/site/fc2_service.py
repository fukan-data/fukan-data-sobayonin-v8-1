import random
import re
from time import sleep
from common.consts.fc2 import FC2
from common.enums.status import Status
from common.services.common_service import CommonService
from common.services.selenium_service import SeleniumService
from common.services.components.decorator import retry as custom_retry
# from common.services.google.big_query import BigQueryService
# from common.services.pyautogui.pyautogui_service import PyAutoGuiService
from common.services.google.spread_sheet_service import SpreadSheetService


class Fc2Service(CommonService):
    def __init__(self, logger=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = self.get_logger() if logger is None else logger
        # self.py_auto_gui = PyAutoGuiService()
        self.selemium = SeleniumService()
        # self.big_query = BigQueryService(logger=self.logger)
        self.spread_sheet = SpreadSheetService(logger=self.logger)

    @custom_retry(delay=1, tries=3, close_driver=1)
    def login(self, driver):
        driver.get(FC2.URL.LOGIN_URL)

        # 登録メールアドレス
        element_email = self.selemium.get_element_with_wait(driver, '//*[@id="email"]')
        element_email.send_keys(FC2.ACCOUNT.CONNECTFAM.USER_NAME)

        # パスワード
        element_pass = self.selemium.get_element_with_wait(driver, '//*[@id="pass"]')
        element_pass.send_keys(FC2.ACCOUNT.CONNECTFAM.PASSWORD)

        # ログイン
        element_btn = self.selemium.get_element_with_wait(driver, '//*[@id="login-content"]/form/ul/li[5]/p/a/input')
        element_btn.click()

        if not self.selemium.is_current_url(driver, FC2.URL.LOGIN_AFTER_URL):
            message = 'Can\'t login fc2 live'
            self.logger.error(message)
            return Status.get_response(status=Status.FAIL_TO_LOGIN, detail=message)

        return driver

    @custom_retry(delay=1, tries=3, close_driver=1)
    def search_performers(self, driver):
        driver.get(FC2.URL.PERFORMER_SEARCH)

        res = {}

        for element_tr in self.selemium.get_element_with_wait(driver, '//*[@id="result"]//tr', is_multiple=True):

            id = ''
            name_sei = ''
            name_mei = ''
            nick_name = ''
            belong = ''
            favorite_by = ''
            point = ''
            personal_url = ''
            point_url = ''

            for i, element_td in enumerate(self.selemium.get_element_with_wait(element_tr, './td', is_multiple=True)):
                text = element_td.text
                href = ''

                try:
                    element_td_a = self.selemium.get_element_with_wait(element_td, './a')
                    href = element_td_a.get_attribute('href')
                except:
                    pass

                if i == 0:
                    belong = text
                elif i == 1:
                    id = text
                elif i == 2:
                    nick_name = text
                    personal_url = href
                elif i == 3:
                    name_sei_mei = text.split(' ')
                    name_sei = name_sei_mei[0]
                    name_mei = name_sei_mei[1]
                elif i == 4:
                    favorite_by = text.replace('人', '')
                elif i == 5:
                    point = text.replace('pt', '')
                    point_url = href

            if id == '':
                continue

            res[id] = {
                'id': id,
                'name_sei': name_sei,
                'name_mei': name_mei,
                'nick_name': nick_name,
                'belong': belong,
                'favorite_by': favorite_by,
                'point': point,
                'personal_url': personal_url,
                'point_url': point_url,
            }

        return res

    @custom_retry(delay=1, tries=3, close_driver=1)
    def search_performer_basic(self, driver, performer_dict):
        driver.get(performer_dict['personal_url'])

        info_dict = {
            'メールアドレス': 'email',
            'ログインID': 'login_id',
            'ログインパスワード': 'login_password',
            '本名（漢字）': 'name',
            '本名（カナ）': 'name_kana',
            '生年月日': 'birth_day',
            '連絡先': 'contact',
            '身分証明書': 'identification',
            '国・地域': 'country_place',
            '報酬割合': 'reward_ratio',
            '配信停止措置※1': 'stop_type',
        }

        for element_tr in self.selemium.get_element_with_wait(driver, '//*[@id="otheresetting"]//tr', is_multiple=True):

            element_th = self.selemium.get_element_with_wait(element_tr, './th')
            item_name = element_th.text
            item_key = info_dict[item_name]
            element_td = self.selemium.get_element_with_wait(element_tr, './td')
            item_value = element_td.text
            performer_dict[item_key] = item_value

            if item_key == 'email':
                performer_dict['email'] = item_value.split('\n')[0]

            elif item_key == 'login_id':
                performer_dict['login_id'] = item_value.split('\n')[0]

            elif item_key == 'name':
                # 姓
                element_name_sei = self.selemium.get_element_with_wait(element_tr, '//*[@id="realName_l"]')
                performer_dict['name_sei'] = element_name_sei.get_attribute('value')
                # 名
                element_name_mei = self.selemium.get_element_with_wait(element_tr, '//*[@id="realName_f"]')
                performer_dict['name_mei'] = element_name_mei.get_attribute('value')

            elif item_key == 'name_kana':
                # 姓
                element_name_sei = self.selemium.get_element_with_wait(element_tr, '//*[@id="nameKana_l"]')
                performer_dict['name_kana_sei'] = element_name_sei.get_attribute('value')
                # 名
                element_name_mei = self.selemium.get_element_with_wait(element_tr, '//*[@id="nameKana_f"]')
                performer_dict['name_kana_mei'] = element_name_mei.get_attribute('value')

            elif item_key == 'birth_day':
                # 生年月日　年
                element_birth_y = self.selemium.get_element_with_wait(element_tr, '//*[@id="birth_y"]')
                # 生年月日　月
                element_birth_m = self.selemium.get_element_with_wait(element_tr, '//*[@id="birth_m"]')
                # 生年月日　日
                element_birth_d = self.selemium.get_element_with_wait(element_tr, '//*[@id="birth_d"]')

                performer_dict['birth_day'] = '{}/{}/{}'.format(
                    element_birth_y.get_attribute('value'), element_birth_m.get_attribute('value'), element_birth_d.get_attribute('value'))

            elif item_key == 'contact':
                element_contact = self.selemium.get_element_with_wait(element_tr, '//*[@id="contactInfo"]')
                performer_dict['contact'] = element_contact.get_attribute('value')

            elif item_key == 'reward_ratio':
                element_reward_ratio = self.selemium.get_element_with_wait(element_tr, '//*[@id="distribute"]')
                performer_dict['reward_ratio'] = element_reward_ratio.get_attribute('value')

        return performer_dict

    @custom_retry(delay=1, tries=3, close_driver=1)
    def search_performer_point(self, driver, performer_dict):
        driver.get(performer_dict['point_url'])

        # 年月
        element_caption = self.selemium.get_element_with_wait(driver, '//*[@id="main_2col"]//caption')
        element_caption_value = element_caption.text
        caption_value = re.sub('[前の月次の月 «»]', '', element_caption_value)
        caption_start = caption_value.split('~')[0]
        caption_year_month = caption_start.split('-')
        start_year = caption_year_month[0]
        start_month = caption_year_month[1]

        # ポイント最新月
        res = []
        for element_tr in self.selemium.get_element_with_wait(driver, '//*[@id="main_2col"]//tr', is_multiple=True):

            res_date = ''
            res_chat = ''
            res_tip = ''
            res_sum = ''

            for i, element_td in enumerate(self.selemium.get_element_with_wait(element_tr, './td', is_multiple=True)):
                item_value = element_td.text

                if i == 0:
                    res_date = '{}/{}/{}'.format(start_year, start_month, item_value.split('(')[0])
                elif i == 1:
                    res_chat = item_value
                elif i == 2:
                    res_tip = item_value
                elif i == 3:
                    res_sum = item_value
            if res_date == '':
                continue
            elif res_date.find('合計') > -1:
                performer_dict['points_sum'] = res_chat
                performer_dict['points_sheet_name'] = '{}{}01'.format(start_year, start_month)
            else:
                res.append([res_date, res_chat, res_tip, res_sum])

        performer_dict['points'] = res

        return performer_dict

    @custom_retry(delay=1, tries=3, close_driver=1)
    def set_performer_info(self, performers_dict):
        sheet_id = '1qt5CYJCjh3Xbj3E8tZiUN8DoFp0jpkXkL3wV8auYl1k'
        sheet_name = 'パフォーマー'
        sheet_range = 'A2:T'
        sheet_records = self.spread_sheet.get_values(sheet_id, sheet_name, sheet_range)

        sheet_id_sheet_name = 'シートID'
        sheet_id_sheet_range = 'A2:B'
        sheet_ids = {}
        for record in self.spread_sheet.get_values(sheet_id, sheet_id_sheet_name, sheet_id_sheet_range).data['values']:
            sheet_ids[str(record[0])] = record[1]

        records = []
        for record in sheet_records.data['values']:
            id = str(record[0])
            is_target = False
            for performer_dict in performers_dict.values():
                if id == performer_dict['id']:
                    is_target = True
                    records.append([
                        performer_dict['id'],  # : '84909097'
                        performer_dict['belong'],  # : 'JOY LLC'
                        performer_dict['nick_name'],  # : 'ふうか'
                        performer_dict['name_sei'],  # : : '清水'
                        performer_dict['name_mei'],  # : : '柚香'
                        performer_dict['name_kana_sei'],  # : 'シミズ'
                        performer_dict['name_kana_mei'],  # : 'ユウカ'
                        performer_dict['email'],  # : 'mt90zig8em89ie@live.fc2.com'
                        performer_dict['login_id'],  # : 'ig8em89ie'
                        performer_dict['login_password'],  # : 'qY9bZ0uU'
                        performer_dict['birth_day'],  # : '2000/11/22'
                        performer_dict['contact'],  # : '':
                        performer_dict['identification'],  # : '身分証明書追加登録'
                        performer_dict['country_place'],  # : '配信除外国・地域指定'
                        performer_dict['reward_ratio'],  # : '35'
                        performer_dict['stop_type'],  # : '何もしない 12時間 24時間'
                        performer_dict['favorite_by'],  # : '242'
                        performer_dict['point'],  # : '61365'
                        performer_dict['personal_url'],  # : 'https://live.fc2.com/manage/performer_edit/?cid=38488828'
                        performer_dict['point_url'],  # : 'https://live.fc2.com/manage/monthly/?managerId=38316275&castId=38488828'
                    ])

            if not is_target:
                records.append(record)

        # スプレッドシートへの記録
        self.spread_sheet.set_values(sheet_id, sheet_name, sheet_range, records)

        # 値の更新
        for performer_dict in performers_dict.values():
            sheet_id = sheet_ids[performer_dict['id']]
            sheet_name = performer_dict['points_sheet_name']
            records = [['年月日', 'チャット', 'チップ', '合計']]
            records.extend(performer_dict['points'])
            sheet_range = 'A:D'
            self.spread_sheet.update_sheet(sheet_id, sheet_name, sheet_range, records)

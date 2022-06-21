import os
from selenium.webdriver.common.keys import Keys
from time import sleep

from common.consts.instagram import INSTAGRAM
from common.enums.status import Status
from common.services.common_service import CommonService
from common.services.selenium_service import SeleniumService
from common.services.components.system_exception import SystemException
from common.services.components.decorator import retry as custom_retry
from common.services.google.big_query import BigQueryService


class InstagramService(CommonService):
    def __init__(self, logger=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = self.get_logger() if logger is None else logger
        self.selemium = SeleniumService()
        self.big_query = BigQueryService(logger=self.logger)

    @custom_retry(delay=1, tries=3, close_driver=1)
    def login(self, driver):
        driver = self.selemium.login_google(driver=driver)
        driver.get(INSTAGRAM.URL.LOGIN_URL)

        # ブラウザがログイン状態ならdriverを返して終了
        if driver.current_url == INSTAGRAM.URL.BASE_URL:
            return

        # ログイン username
        xpath_username = '//*[@id="loginForm"]//input[@name="username"]'
        element_username = self.selemium.get_element_with_wait(driver, xpath_username)
        self.selemium.clear(element_username)
        element_username.send_keys(INSTAGRAM.ACCOUNT.CONNECTFAM.USER_NAME)

        # ログイン password
        xpath_password = '//*[@id="loginForm"]//input[@name="password"]'
        element_password = self.selemium.get_element_with_wait(driver, xpath_password)
        self.selemium.clear(element_password)
        element_password.send_keys(INSTAGRAM.ACCOUNT.CONNECTFAM.PASSWORD)

        # ログイン submit
        xpath_submit = '//*[@id="loginForm"]//button[@type="submit"]'
        element_submit = self.selemium.get_element_with_wait(driver, xpath_submit)
        element_submit.click()

        # ログイン後 urlの確認
        if INSTAGRAM.URL.LOGIN_AFTER_URL not in driver.current_url:
            raise SystemException(status=Status.FAIL_TO_LOGIN, message='パスワードが異なっている可能性があります。', tries=3)

        return

    # @custom_retry(delay=1, tries=3, close_driver=1)
    def read_page(self, driver, page_name):
        driver.get(INSTAGRAM.URL.BASE_URL + page_name)

        # wait untilの実装が必要
        xpath_h2 = '//h2[contains(text(), "connectfam9")]'
        self.selemium.wait_until(driver, xpath_h2)

        # 写真一覧の各写真をクリック
        xpath_article = '//article//a'
        for element_article in self.selemium.get_element_with_wait(driver, xpath_article, is_multiple=True):
            element_article.click()
            sleep(1)

            main_comments = []
            hash_tags = []
            at_tags = []

            # 画像のダウンロード
            xpath_img = '//*[@role="button"]//img'
            image_data = self.selemium.save_image(driver, xpath_img, stock_dir='instagram/' + page_name)

            # コメントを抽出
            xpath_span_parent = '//*[@role="menuitem"]//span/../..'
            for element_span_parent in self.selemium.get_element_with_wait(element_article, xpath_span_parent, is_multiple=True):
                comment = element_span_parent.text
                if comment == '':
                    continue
                # #model @modelのようなタグ付きのリンクを取得
                xpath_a = './/a'
                for element_a in self.selemium.get_element_with_wait(element_span_parent, xpath_a, is_multiple=True):
                    element_a_text = element_a.text
                    if element_a_text[0:1] == '#':
                        hash_tags.append(element_a_text)
                    if element_a_text[0:1] == '@':
                        at_tags.append(element_a_text)
                # 自分自身の場合が投稿したのかを確認(h2に誰が投稿したか存在)
                try:
                    xpath_h2 = './/h2'
                    element_h2 = element_span_parent.find_element_by_xpath(xpath_h2)
                    if page_name == element_h2.text:
                        main_comments.append(comment)
                except Exception as e:
                    pass
            main_comment = '\n>>>コメント結合>>>\n'.join(main_comments)

            # //*[@role="menuitem"]//span
            rows = [{
                'page_name': page_name,
                'pc': self.PC_NAME,
                'main_comment': main_comment,
                'hash_tags': hash_tags,
                'at_tags': at_tags,
                'image_file_path': image_data['file_path'],
                'image_width': image_data['width'],
                'image_height': image_data['height'],
            }]

            table_id = ''
            self.big_query.insert_rows(table_id=table_id, rows=rows)




    """
    @custom_retry(delay=1, tries=1)
    def throw(self, id, file_name, message):

        aaa = self.encode_space_identifier(20, start='>', end='.')
        print('>>>', aaa)
        aaa2 = self.decode_space_identifier(aaa, start='>', end='.')
        print('===', aaa2)
        # return



        # # ログイン
        # login_response = self.login()
        # if login_response.status != Status.SUCCESS.no:
        #     raise SystemException(status_id=login_response.status)
        # driver = login_response.data

        # ダイアログの表示があった場合
        try:
            xpath = '//*[@role="dialog"]//*[contains(text(), "後で")]'
            element = self.selemium.get_element_with_wait_short(driver, xpath)
            element.click()
        except Exception as e:
            pass


        # 投稿済みのデータかを確認

        # 「続きを読む」ボタンを選択
        # //*[@id="react-root"]/section/main/section/div[1]/div[2]/div[1]/div/article[1]/div/div[3]/div/div/div[1]/div/div[1]/div/span[3]/span[2]/div



        # //*[@id="react-root"]/section/main/section/div[1]/div[2]/div[1]/div/article[1]/div/div[3]/div/div/div[1]/div/div[1]/div/span[3]/span
        # //*[contains(text(), "続きを読む")]
        # //*[contains(text(), "続きを読む")]/../../../../span[3]/span
        # //*[contains(text(), "CONNECTFAMでは、ポートレート撮影を随時行なっています📸🥼👗")]


        # プラスボタンを選択
        xpath_plus = '//*[@id="react-root"]//nav//button'
        element_plus = self.selemium.get_element_with_wait(driver, xpath_plus)
        element_plus.click()

        # ファイルを選択する
        xpath_file = '//*[@aria-label="新規投稿を作成"]//form[@role="presentation"]//input[@type="file"]'
        element_file = self.selemium.get_element_with_wait(driver, xpath_file)
        path_to_image = os.path.join(INSTAGRAM.PATH.DIR.STOCK, file_name)
        element_file.send_keys(path_to_image)

        # 次へを選択する
        xpath = '//*[@aria-label="切り取る"]//button[contains(text(), "次へ")]'
        element = self.selemium.get_element_with_wait(driver, xpath)
        element.click()

        # 次へを選択する
        xpath = '//*[@aria-label="編集"]//button[contains(text(), "次へ")]'
        element = self.selemium.get_element_with_wait(driver, xpath)
        element.click()

        # 投稿メッセージの入力
        xpath = '//*[@aria-label="新規投稿を作成"]//textarea'
        element = self.selemium.get_element_with_wait(driver, xpath)
        element.send_keys(Keys.RETURN)
        driver.execute_script(self.selemium.get_js_text('send_text'), element, message)
        element.send_keys(Keys.RETURN)

        # シェアボタンを選択
        xpath = '//*[@aria-label="新規投稿を作成"]//button[contains(text(), "シェア")]'
        element = self.selemium.get_element_with_wait(driver, xpath)
        element.click()

        # 投稿が終わるまで待つ
        for i in range(10):
            xpath = '//*[@aria-label="投稿をシェアしました"]//h2'
            element = self.selemium.get_element_with_wait(driver, xpath)
            if '投稿がシェアされました。' in element.text:
                break
            sleep(1)

        # 終了
        self.selemium.quit(driver)
    """

from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.keys import Keys
import pyautogui
import random
import re
from time import sleep
import urllib.parse

from common.consts.instagram import INSTAGRAM
from common.enums.status import Status
from common.services.common_service import CommonService
from common.services.selenium_service import SeleniumService
from common.services.components.system_exception import SystemException
from common.services.components.decorator import retry as custom_retry
from common.services.google.big_query import BigQueryService
from common.services.pyautogui.pyautogui_service import PyAutoGuiService
from common.services.google.spread_sheet_service import SpreadSheetService

from selenium.webdriver.common.action_chains import ActionChains


class InstagramService(CommonService):
    def __init__(self, logger=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = self.get_logger() if logger is None else logger
        self.py_auto_gui = PyAutoGuiService()
        self.selemium = SeleniumService()
        self.big_query = BigQueryService(logger=self.logger)
        self.spread_sheet = SpreadSheetService(logger=self.logger)

    @custom_retry(delay=1, tries=3, close_driver=1)
    def login(self, driver):
        driver = self.selemium.login_google(driver=driver)
        driver.get(INSTAGRAM.URL.LOGIN_URL)

        # ブラウザがログイン状態ならdriverを返して終了
        if driver.current_url == INSTAGRAM.URL.BASE_URL:
            self.__close_dialog(driver)
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

        self.__close_dialog(driver)
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

    def __goto_next(self, driver):
        # 次へ
        xpath_next = '//div[@role="dialog"]//button//*[name()="svg"][@aria-label="次へ"]/../../..'
        element_next = self.selemium.get_element_with_wait(driver, xpath_next)
        element_next.click()
        sleep(2 + (2 * random.random()))

    def __close_dialog(self, driver):
        try:
            xpath_next = '//*[@role="dialog"]//button[contains(text(), "後で")]'
            element_next = driver.find_element_by_xpath(xpath_next)
            element_next.click()
            self.logger.info('End of close_dialog')
        except Exception as e:
            self.logger.info('No dialog')

    def __get_page_id(self, url):
        url_splits = url.replace('https://www.instagram.com/', '').split('/')

        # case: https://www.instagram.com/p/CfRS4Fsrn4l/
        if url_splits[0] == 'p':
            return url_splits[1]
        else:
            return None

    # @custom_retry(delay=1, tries=3, close_driver=1)
    def search_tag(self, driver, key_word, select_hash_list, max_count):
        # キーワードのページへ遷移
        key_word_quote = urllib.parse.quote(key_word)
        driver.get('https://www.instagram.com/explore/tags/' + key_word_quote + '/')

        # wait untilの実装が必要
        xpath_h1 = '//section//h1'
        self.selemium.wait_until(driver, xpath_h1)

        # 投稿内容の一覧を取得
        xpath_a_throw = '//a[@role="link"]'
        element_a_throw = self.selemium.get_element_with_wait(driver, xpath_a_throw)
        element_a_throw.click()
        sleep(2)

        # スプレッドシートへの記録
        sheet_id = '1Ni5JzhqCNdLTSW-izJzRh92VGPzPZRGuVlBpUl1p9bE'
        # sheet_name = '20220626'
        sheet_name = '20220703'
        sheet_range = 'A:G'
        sheet_records = self.spread_sheet.get_values(sheet_id, sheet_name, sheet_range)

        sheet_info = {}
        for record in sheet_records.data['values']:
            if record[0] != '取得元' and record[0] != 'error':
                try:
                    sheet_info[self.__get_page_id(record[4])] = {
                        'count': int(record[1]) if record[1] else 0,
                        'error': True if record[5] == '' else False
                    }
                except Exception as e:
                    print('Error: ', record)

        # 繰り返しする
        count = 0
        while count < max_count:
            try:
                scrape_count = 1

                # シートの中に既存のurlがある場合
                page_id = self.__get_page_id(driver.current_url)
                if page_id in sheet_info:
                    thrower_info = sheet_info[page_id]
                    # エラーかつ3回以内なら再実行
                    if (thrower_info['error'] and thrower_info['count'] < 3):
                        scrape_count = int(thrower_info['count']) + 1
                    else:
                        self.__goto_next(driver)
                        continue

                # 投稿者
                thrower = ''
                xpath_header = '//article//header//a[@role="link"]'
                for element_header in self.selemium.get_element_with_wait(element_a_throw, xpath_header, is_multiple=True):
                    if not thrower:
                        thrower = element_header.text

                # ハッシュを取得する
                hash_list = []
                xpath_hash = '//a[contains(text(), "#")]'
                for element_hash in self.selemium.get_element_with_wait(element_a_throw, xpath_hash, is_multiple=True):
                    hash_list.append(element_hash.text)

                # ハッシュタグがselect_hash_listに存在していれば、「いいね」の対象とする
                is_like_target = False
                for select_hash in select_hash_list:
                    for hash in hash_list:
                        if select_hash in hash:
                            is_like_target = True
                            break

                # いいねの対象
                like = ''
                if is_like_target:
                    xpath_like = '//article//section//button'
                    element_like = self.selemium.get_element_with_wait(driver, xpath_like)
                    element_like.click()
                    like = 'いいね'

                # スプレッドシートへの記録
                values = [thrower, scrape_count, like, '', driver.current_url, ', '.join(hash_list)]
                self.spread_sheet.append_row(sheet_id, sheet_name, values)

                # 次へ
                self.__goto_next(driver)

                count += 1

            except Exception as e:
                # スプレッドシートへの記録
                values = ['error', '', '', '', '', '', e.__str__()]
                self.spread_sheet.append_row(sheet_id, sheet_name, values)

    # @custom_retry(delay=1, tries=3, close_driver=1)
    def search_followers(self, driver, page_name):
        # キーワードのページへ遷移
        driver.get('https://www.instagram.com/' + page_name + '/')

        # wait untilの実装が必要
        xpath_follower_link = '//header/section/ul/li/a'
        self.selemium.wait_until(driver, xpath_follower_link)

        # 投稿内容の一覧を取得
        element_a_throw = self.selemium.get_element_with_wait(driver, xpath_follower_link)
        element_a_throw.click()
        sleep(2)

        # フォロワーを取得
        xpath_followers = '//*[@role="dialog"]//*[@role="dialog"]//ul//li//a/span'
        followers = []
        count_followers = -1
        is_end = False

        while not is_end:
            for element_followers in self.selemium.get_element_with_wait(element_a_throw, xpath_followers, is_multiple=True):
                followers.append(element_followers.text)
            followers = list(set(followers))

            if count_followers == len(followers):
                is_end = True
            count_followers = len(followers)

            # フォロワーをスクロール
            xpath_follower_scroll = '//*[@role="dialog"]//*[@role="dialog"]//ul/following-sibling::div'
            element_follower_scroll = self.selemium.get_element_with_wait(driver, xpath_follower_scroll)
            driver.execute_script("arguments[0].scrollIntoView(true);", element_follower_scroll)
            sleep(3)

        # スプレッドシートへの記録
        sheet_id = '1Ni5JzhqCNdLTSW-izJzRh92VGPzPZRGuVlBpUl1p9bE'
        sheet_name = 'followers'
        sheet_range = 'A2:A'

        follower_list = []
        for follower in followers:
            follower_list.append([follower])
        sheet_range = sheet_range + str(len(follower_list) + 2)
        # self.spread_sheet.append_row(sheet_id, sheet_name, follower_list)
        self.spread_sheet.set_values(sheet_id, sheet_name, sheet_range, follower_list)

        pass

    def read_instagram_position(self, chrome_position):
        try:
            # # image_path = './common/services/pyautogui/image/chrome_left_up.png'
            # chrome_left_up_path = './common/services/pyautogui/image/chrome_left_up.png'
            # chrome_left_up = pyautogui.locateOnScreen(chrome_left_up_path)
            # print('_______', chrome_left_up)
            #
            # chrome_right_bottom_path = './common/services/pyautogui/image/chrome_right_bottom.png'
            # chrome_right_bottom = pyautogui.locateOnScreen(chrome_right_bottom_path)
            # print('_______', chrome_right_bottom)
            #
            # chrome_search_path = './common/services/pyautogui/image/chrome_search.png'
            # x, y = pyautogui.locateCenterOnScreen(chrome_search_path)
            # print('_______', x, y)
            #
            # return {
            #     'top': chrome_left_up.top,
            #     'left': chrome_left_up.left,
            #     'right': chrome_right_bottom.left + chrome_right_bottom.width,
            #     'bottom': chrome_right_bottom.top + chrome_right_bottom.height,
            #     'search': {
            #         'x': x,
            #         'y': y
            #     }
            # }
            pass

        except Exception as ex:
            print("[read_chrome] 対象が見つかりませんでした。")
            print(ex)

    def search_tag_direct(self, page_name, key_word, select_hash_list, max_count):
        thrower = ''
        hash_list = []
        current_url = ''

        # スプレッドシートへの記録
        sheet_id = '1Ni5JzhqCNdLTSW-izJzRh92VGPzPZRGuVlBpUl1p9bE'
        sheet_name = '20220719'
        sheet_range = 'A:G'
        sheet_records = self.spread_sheet.get_values(sheet_id, sheet_name, sheet_range)

        sheet_info = {}
        for record in sheet_records.data['values']:
            if record[0] != '取得元' and record[0] != 'error':
                try:
                    sheet_info[self.__get_page_id(record[4])] = {
                        'count': int(record[1]) if record[1] else 0,
                        'error': True if record[5] == '' else False
                    }
                except Exception as e:
                    print('Error: ', record)

        brower = 'edge'
        image_path = './common/services/pyautogui/image/icon_edge_taskbar.png'
        chrome_position = self.py_auto_gui.start_chrome(image_path, browser=brower)
        print(chrome_position)

        # instagram_position = self.read_instagram_position(chrome_position)

        # url = 'https://www.instagram.com/' + page_name + '/'
        # self.py_auto_gui.open_chrome(x, y, url)

        # キーワードのページへ遷移
        key_word_quote = urllib.parse.quote(key_word)
        url = 'https://www.instagram.com/explore/tags/' + key_word_quote + '/'
        x = chrome_position['search']['x']
        y = chrome_position['search']['y']
        # url = 'https://www.yosakoi-soran.jp/'
        self.py_auto_gui.open_chrome(x, y, url)
        sleep(10)

        # 投稿画像をクリック
        x = 300
        y = 600
        self.py_auto_gui.click(x, y)

        # 開発モードを開く
        self.py_auto_gui.open_develop_mode()

        # 繰り返しする
        count = 0
        while count < max_count:
            try:
                scrape_count = 1

                # url取得
                x = chrome_position['search']['x']
                y = chrome_position['search']['y']
                current_url = self.py_auto_gui.copy_text(x, y)
                print('current_url', current_url)

                x = 800
                y = 550
                scroll_to = random.uniform(200, 0)
                # self.py_auto_gui.dummy_scroll(x, y, random_x=10, random_y=10, scroll_to=scroll_to)
                # article = self.py_auto_gui.copy_text(x, y)

                x = 820
                y = 230
                article = self.py_auto_gui.copy_dom(x, y)
                sleep(1 + 2 * random.random())
                sleep(300)

                # いいね画像ボタン
                x = 697
                y = 760
                image_path = './common/services/pyautogui/image/edge_like.png'
                self.py_auto_gui.click_image(image_path=image_path, x=x, y=y, random_x=5, random_y=5)

                # 記事の読み込み
                values = self.read_article(thrower, page_name, article, current_url, scrape_count)
                print(values)

                # スプレッドシートへの記録
                self.spread_sheet.append_row(sheet_id, sheet_name, values)

            except Exception as e:
                print(e.__str__())
                # スプレッドシートへの記録
                values = ['error', '', '', '', '', '', e.__str__()]
                self.spread_sheet.append_row(sheet_id, sheet_name, values)

            # 次の画像ボタン
            x = 1181
            y = 569
            image_path = './common/services/pyautogui/image/edge_next.png'
            self.py_auto_gui.click_image(image_path=image_path, x=x, y=y, random_x=5, random_y=5)

            sleep(4 + 3 * random.random())
            count += 1

    def search_tag_dev_mode(self, page_name, key_word, select_hash_list, max_count):
        error_count = 0

        for i in range(100):
            try:
                # スプレッドシートへの記録
                sheet_id = '1Ni5JzhqCNdLTSW-izJzRh92VGPzPZRGuVlBpUl1p9bE'
                sheet_name = '20220722'
                sheet_range = 'A:G'
                sheet_records = self.spread_sheet.get_values(sheet_id, sheet_name, sheet_range)

                sheet_info = {}
                read_count = 0
                for record in sheet_records.data['values']:
                    if record[0] != '取得元' and record[0] != 'error':
                        try:
                            sheet_info[self.__get_page_id(record[4])] = {
                                'count': int(record[1]) if record[1] else 0,
                                'error': True if record[5] == '' else False
                            }
                            read_count += 1
                        except Exception as e:
                            print('Error: ', record)

                # 初回のみブラウザ起動とインスタの投稿画面を表示
                if i == 0:
                    brower = 'edge'
                    image_path = './common/services/pyautogui/image/icon_edge_taskbar.png'
                    chrome_position = self.py_auto_gui.start_chrome(image_path, browser=brower)
                    print(chrome_position)

                    # 開発モードを開く
                    x = 790
                    y = 130
                    self.py_auto_gui.open_develop_mode(x=x, y=y, type='pc')

                    # キーワードのページへ遷移
                    key_word_quote = urllib.parse.quote(key_word)
                    url = 'https://www.instagram.com/explore/tags/' + key_word_quote + '/'
                    x = chrome_position['search']['x']
                    y = chrome_position['search']['y']
                    self.py_auto_gui.open_chrome(x, y, url)
                    sleep(10)

                    # 画面をクリック
                    x = 200
                    y = 300
                    self.py_auto_gui.click(x, y)
                    sleep(0.5)

                    # 投稿画像をクリック
                    x = 200
                    y = 550
                    self.py_auto_gui.click(x, y)
                    sleep(3)

                # 繰り返しする
                count = 0
                while count < max_count:
                    skip_count = 1
                    try:
                        if count != 0 and count % 31 == 0:
                            print('sleep time')
                            sleep(int(120 + 150 * random.random()))

                        # 連続5回の失敗で終了
                        if error_count > 4:
                            max_count = 0
                            continue

                        scrape_count = 1

                        # url取得
                        x = chrome_position['search']['x']
                        y = chrome_position['search']['y']
                        current_url = self.py_auto_gui.copy_text(x, y)
                        print('current_url', current_url)

                        # URLが開いていたときの回避
                        x = 900
                        y = 350
                        pyautogui.moveTo(x, y, duration=0.25)
                        pyautogui.click()

                        throw_id = self.get_throw_id(current_url)
                        print(throw_id)

                        # throw_idが未登録の場合
                        if throw_id not in sheet_info:
                            x = 824
                            y = 141
                            article = self.py_auto_gui.copy_dom(x, y)
                            sleep(1 + 2 * random.random())
                            sleep(3)
                            # print(article)

                            self.save_article_dom(throw_id, article)

                            # 記事の読み込み
                            values = self.read_article_dom(key=throw_id, scrape_count=scrape_count, current_url=current_url)
                            print(values)

                            if values[0] == '':
                                raise Exception('Cannot get thrower from article')

                            # いいね画像ボタン
                            x = 227
                            y = 499
                            image_path = './common/services/pyautogui/image/edge_like.png'
                            self.py_auto_gui.click_image_curve(image_path=image_path, x=x, y=y)
                            # self.py_auto_gui.click_image(image_path=image_path, x=x, y=y, random_x=5, random_y=5)

                            # # 記事の読み込み
                            # values = self.read_article(thrower, page_name, article, current_url, scrape_count)
                            # print(values)

                            # スプレッドシートへの記録
                            self.spread_sheet.append_row(sheet_id, sheet_name, values)
                            count += 1
                            error_count = 0
                        else:
                            # 更新処理回数分に達するまでは20回ずつスキップする
                            if read_count > 0:
                                read_count -= 20
                                skip_count = 20
                            else:
                                skip_count = 1

                    except Exception as e:
                        print(e.__str__())
                        # スプレッドシートへの記録
                        values = ['error', '', '', '', '', '', e.__str__()]
                        self.spread_sheet.append_row(sheet_id, sheet_name, values)
                        count += 1
                        error_count += 1

                    # count += 1
                    # continue

                    # 次の画像ボタン
                    x = 716
                    y = 405
                    self.py_auto_gui.click_image_curve(x=x, y=y, count=skip_count)
                    # image_path = './common/services/pyautogui/image/edge_next.png'
                    # self.py_auto_gui.click_image(image_path=image_path, x=x, y=y, random_x=5, random_y=5)

                    sleep(4 + 3 * random.random())

            except Exception as e:
                print(e.__str__())

    def search_tag_android_mode(self, page_name, key_word, select_hash_list, max_count):

        # This Python file uses the following encoding: utf-8
        # pip install android-auto-play-opencv
        import android_auto_play_opencv as am
        adbpath = 'platform-tools\\'

        aapo = am.AapoManager(adbpath)
        while True:
            # 画面キャプチャ
            aapo.screencap()










    def get_article_dom(self, file_path):
        try:
            with open(file_path, mode='r', encoding='UTF-8') as fp:
                return fp.read()
        except Exception as e:
            return None

    def save_article_dom(self, key, article):
        # ファイルの保存
        os.makedirs('common/services/pyautogui/dom', exist_ok=True)
        file_path = 'common/services/pyautogui/dom/article_' + key + '.txt'
        if not os.path.exists(file_path):
            with open(file_path, mode='w', encoding='UTF-8') as f:
                f.write(article)

    def read_article_dom(self, key=None, article=None, scrape_count=1, current_url=''):
        hash_list = []
        like = 'いいね'
        thrower = ''

        if article is None:
            os.makedirs('common/services/pyautogui/dom', exist_ok=True)
            file_path = 'common/services/pyautogui/dom/article_' + key + '.txt'
            article = self.get_article_dom(file_path)

        # BeautifulSoup
        soup = BeautifulSoup(article, 'html.parser')
        # article
        for element_article in soup.find_all('article'):
            for element_a in element_article.find_all('a'):
                element_a_text = element_a.text
                if '#' in element_a_text:
                    hash_list.append(element_a_text)

                for element_a_img in element_a.find_all('img'):
                    element_a_alt = element_a_img.get('alt')
                    # プロフィール写真を含むa>imgがあること、かつ、hash_listに未登録の最初の人であること
                    if element_a_alt and 'のプロフィール写真' in element_a_alt and len(hash_list) == 0:
                        thrower = element_a_alt.replace('のプロフィール写真', '')

        # スプレッドシートへの記録
        return [thrower, scrape_count, like, '', current_url, ', '.join(hash_list), '']

    def get_throw_id(self, url):
        throw_id = url.replace('https://www.instagram.com/p/', '')
        return throw_id.replace('/', '')

    def read_article(self, thrower, page_name, article, current_url, scrape_count):
        try:
            hash_list = []
            like = 'いいね'
            for article in article.split('のプロフィール写真'):
                lines = article.splitlines()
                person = lines[0] or lines[1]

                # 不要ページをジャンプ
                if page_name in article:
                    continue

                if 'Meta' == person:
                    continue

                if thrower == '':
                    thrower = lines[0] or lines[1]

                # 投稿者の記事選択
                if thrower == person:
                    lines.pop()
                    lines.pop()

                    thrower_article = '\n'.join(lines)
                    for hash_line in re.findall('#.*', thrower_article):
                        for hash in hash_line.split(' '):
                            if '#' in hash:
                                hash_list.append(hash)

            # スプレッドシートへの記録
            return [thrower, scrape_count, like, '', current_url, ', '.join(hash_list), '']
        except Exception as e:
            id = current_url.replace('https://www.instagram.com/p/', '').replace('/', '')
            path_w = 'files/article_{}.png'.format(id)
            with open(path_w, mode='w') as f:
                f.write(article)
            raise(e)





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

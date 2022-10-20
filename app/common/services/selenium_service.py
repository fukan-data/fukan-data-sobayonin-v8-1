# import chromedriver_binary
from datetime import datetime
import io
import os
from PIL import Image
from retry import retry
import subprocess
from time import sleep
from urllib import request

# import logging
# import logging.handlers
# from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.consts.google import GOOGLE
from common.services.common_service import CommonService


class SeleniumService(CommonService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.RESIZE_IMAGE_MAX_WIDTH = 250
        self.RESIZE_IMAGE_MAX_HEIGHT = 250
        self.FILE_PATH_SELENIUM = self.FILE_PATH_STOCK + '/selenium'

    def get_driver(self):
        options = Options()
        env_type = 1  # local
        profilefolder = '--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data'
        if env_type == 1:
            chromedriver_path = os.path.join(os.path.dirname(__file__), '../../chromedriver.exe')
            options.add_argument(profilefolder)
            options.add_argument('--log-level=3')
        else:
            chromedriver_path = '/usr/lib/chromium/chromedriver'
            options.binary_location = '/usr/bin/chromium-browser'
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')

        options.add_argument('--window-size=1200x600')
        return webdriver.Chrome(chromedriver_path, options=options)

    # @retry(delay=1, tries=30, backoff=2, max_delay=4)
    def get_element_with_wait(self, driver, xpath, is_multiple=False):
        if is_multiple:
            # return driver.find_elements_by_xpath(xpath)
            return driver.find_elements(By.XPATH, xpath)
        else:
            # return driver.find_element_by_xpath(xpath)
            return driver.find_element(By.XPATH, xpath)

    @retry(delay=1, tries=5, backoff=2, max_delay=4)
    def get_element_with_wait_short(self, driver, xpath, is_multiple=False):
        if is_multiple:
            # return driver.find_elements_by_xpath(xpath)
            return driver.find_elements(By.XPATH, xpath)
        else:
            # return driver.find_element_by_xpath(xpath)
            return driver.find_element(By.XPATH, xpath)

    @retry(delay=1, tries=3)
    def save_image(self, driver, xpath, stock_dir='system', width=None, height=None):
        element_img = self.get_element_with_wait(driver, xpath)
        img_url = element_img.get_attribute('src')
        f = io.BytesIO(request.urlopen(img_url).read())
        img = Image.open(f)

        # widthとheightは、指定がなければwidthを優先し、デフォルト値に対する縦横比を計算する
        if width is None:
            if height is None:
                width = self.RESIZE_IMAGE_MAX_WIDTH
                height = round(img.height * width / img.width)
                if height > self.RESIZE_IMAGE_MAX_HEIGHT:
                    height = self.RESIZE_IMAGE_MAX_HEIGHT
                    width = round(img.width * height / img.height)
            else:
                width = round(img.width * height / img.height)
        elif height is None:
            height = round(img.height * width / img.width)

        # file_nameはlocalに保存
        file_name = datetime.now(self.get_timezone()).strftime("%Y-%m-%d_%H%M%S")
        file_dir = '{}/{}'.format(self.FILE_PATH_SELENIUM, stock_dir)
        os.makedirs(file_dir, exist_ok=True)
        file_path = '{}/img_{}.png'.format(file_dir, file_name)

        img.resize((width, height)).save(file_path)
        a = 0

        return {
            'width': width,
            'height': height,
            'file_path': file_path,
        }

    def wait_until(self, driver, xpath, timeout=20):
        wait = WebDriverWait(driver=driver, timeout=timeout)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def shut_down_chrome(self):
        print("stop_all_chrome_prcess")
        cmd = 'taskkill /im chrome.exe /f'
        returncode = subprocess.call(cmd)
        print(returncode)
        sleep(5)

    def clear(self, element):
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    # pattern別にjsのtextを取得する
    def get_js_text(self, pattern):
        if pattern == 'send_text':
            return """
                console.log("[get_js_text]", "start");
                try {
                    var elm = arguments[0], txt = arguments[1];
                    elm.value += txt;
                    elm.dispatchEvent(new Event('change'));
                    console.log("[get_js_text]", "success");
                } catch(e) {
                    console.log("[get_js_text]", e.message);
                }
                """

    def quit(self, driver):
        driver.quit()
        driver = None

    def log_critical(self, driver):
        file_name = datetime.now(self.get_timezone()).strftime("%Y%m%d_%H:%M:%S")
        driver.save_screenshot(file_name)

    def login_google(self, driver=None):
        if not driver:
            driver = self.get_driver()
        driver.get(GOOGLE.URL.LOGIN_URL)
        sleep(3)

        # ログイン後 urlの確認
        if GOOGLE.URL.LOGIN_AFTER_URL in driver.current_url:
            return driver

        # TODO: ここから先の処理は、未作成
        xpath = '//*[@id="identifierId"]'
        mail = 'fukan.data.labo@gmail.com'
        element = self.get_element_with_wait(driver, xpath)
        element.send_keys(mail)

        xpath = '//*[@id="identifierNext"]/div/button'
        element = self.get_element_with_wait(driver, xpath)
        element.click()
        sleep(3)

        return driver

    # 一定のURLが対応するまで待機
    def is_current_url(self, driver, target_url, max_count=30):
        count = 0
        while count < max_count:
            if driver.current_url == target_url:
                return True
            sleep(1)
        return False

    def test(self):
        driver = self.login_google()
        driver.get('https://www.tiktok.com/login')

        xpath = '//*[@id="root"]/div/div[1]/div/div[1]/div[2]/div[5]'
        element = self.get_element_with_wait(driver, xpath)
        element.click()
        sleep(3)

        handle_array = driver.window_handles
        driver.switch_to.window(handle_array[1])

        xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div'
        element = self.get_element_with_wait(driver, xpath)
        element.click()
        sleep(3)

        handle_array = driver.window_handles
        driver.switch_to.window(handle_array[0])

        driver.get('https://www.tiktok.com/@samuraishintaro?lang=ja-JP')

        xpath = '//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/div/div[1]'
        element = self.get_element_with_wait(driver, xpath)
        element.click()
        sleep(3)


        sleep(300)


        self.quit(driver)



import os
import pyautogui
import pyperclip
from PIL import ImageGrab
import random
import urllib.parse
from time import sleep
from datetime import datetime

from common.services.common_service import CommonService


class PyAutoGuiService(CommonService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs('./common/services/pyautogui/temporary/', exist_ok=True)
        self.screenshot = ImageGrab.grab()

    def click_icon(self, image_path, x=None, y=None, diff_x=0, diff_y=0, type='left'):
        try:
            if x is None and y is None:
                x, y = pyautogui.locateCenterOnScreen(image_path)
                x = x + diff_x
                y = y + diff_y
            pyautogui.moveTo(x, y, duration=0.25)
            if type == 'right':
                pyautogui.click()
                sleep(0.1)
                pyautogui.rightClick()
            else:
                pyautogui.click(x, y)
        except Exception as ex:
            print("[click_icon] 対象が見つかりませんでした。")
            print(ex)

    def read_chrome_position(self, browser='chrome'):
        try:
            # image_path = './common/services/pyautogui/image/chrome_left_up.png'
            chrome_left_up_path = './common/services/pyautogui/image/' + browser + '_left_up.png'
            chrome_left_up = pyautogui.locateOnScreen(chrome_left_up_path)
            print('1_______', chrome_left_up, chrome_left_up_path)

            chrome_right_bottom_path = './common/services/pyautogui/image/' + browser + '_right_bottom.png'
            chrome_right_bottom = pyautogui.locateOnScreen(chrome_right_bottom_path)
            print('2_______', chrome_right_bottom)

            chrome_search_path = './common/services/pyautogui/image/' + browser + '_search.png'
            x, y = pyautogui.locateCenterOnScreen(chrome_search_path)
            print('3_______', x, y)

            return {
                'top': chrome_left_up.top,
                'left': chrome_left_up.left,
                'right': chrome_right_bottom.left + chrome_right_bottom.width,
                'bottom': chrome_right_bottom.top + chrome_right_bottom.height,
                'search': {
                    'x': x + 50,
                    'y': y
                }
            }

        except Exception as ex:
            print("[read_chrome] 対象が見つかりませんでした。")
            print(ex)

    def start_chrome(self, image_path=None, browser='chrome'):
        today = datetime.now().strftime('%Y%m%d_%H%M%S')
        if image_path is None:
            image_path = './common/services/pyautogui/temporary/screenshot_start_chrome_' + today + '.jpg'
        # self.screenshot.save(image_path)
        # pyautogui.screenshot(image_path)
        # sleep(2)

        # image_path = './common/services/pyautogui/image/icon_chrome_taskbar.png'
        self.click_icon(image_path, x=163, y=752)
        self.click_icon(image_path)
        sleep(3)

        # chrome_position = self.read_chrome_position(browser=browser)
        # print(chrome_position)
        chrome_position = {
            'top': 6,
            'left': 52,
            'right': 1211,
            'bottom': 728,
            'search': {'x': 196, 'y': 60}  # {'x': 287, 'y': 155}
        }
        return chrome_position

    def open_chrome(self, x, y, url):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

    def open_develop_mode(self, x=None, y=None, type='pc'):
        pyautogui.press('f12')
        sleep(3)

        if type == 'pc':
            image_path = './common/services/pyautogui/image/edge_dom_pc.png'
            self.click_icon(image_path, x=x, y=y, diff_x=-15)

    def click2(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def click_image_curve(self, image_path=None, x=227, y=499, count=1):
        try:
            if image_path is not None:
                x, y = pyautogui.locateCenterOnScreen(image_path)
                print(x, y)
        except Exception as e:
            print(e)

        x0, y0 = pyautogui.position()
        diff_x1 = 20 * random.random()
        diff_y1 = 20 * random.random()
        diff_x2 = 5 * random.random()
        diff_y2 = 5 * random.random()
        pyautogui.moveTo((x + x0)/2 + diff_x1, (y + y0)/2 + diff_y1, duration=0.25)
        pyautogui.moveTo(x + diff_x2, y + diff_y2, duration=0.25)

        for i in range(count):
            print('skip count ', count)
            pyautogui.click()
            sleep(0.5 + 0.5 * random.random())

    def click_image(self, image_path=None, x=None, y=None, random_x=10, random_y=10):
        if x is None and y is None:
            try:
                x, y = pyautogui.locateCenterOnScreen(image_path)
                print(x, y)
            except Exception as e:
                print(e)

        self.dummy_move(x, y, random_x=20, random_y=20)
        self.click(x, y, random_x=random_x, random_y=random_y)
        return x, y

    def click(self, x, y, random_x=10, random_y=10):
        # final_x = x + random.uniform(random_x, random_x * -1)
        # final_y = y + random.uniform(random_y, random_y * -1)
        # move1_x = final_x + random.uniform(100, 100 * -1)
        # move1_y = final_y + random.uniform(100, 100 * -1)
        # move2_x = final_x + random.uniform(50, 50 * -1)
        # move2_y = final_y + random.uniform(50, 50 * -1)
        # pyautogui.moveTo(move1_x, move1_y, duration=0.25)
        # pyautogui.moveTo(move2_x, move2_y, duration=0.25)
        # pyautogui.moveTo(final_x, final_y, duration=0.25)
        # sleep(0.2)
        self.dummy_move(x, y, random_x=random_x, random_y=random_y)
        sleep(0.2)
        pyautogui.click()
        # pyautogui.click()
        # pyautogui.mouseDown()
        # sleep(0.2)
        # pyautogui.mouseUp()

    def copy_text(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.click()
        return pyperclip.paste()

    def copy_dom(self, x, y):
        image_path = './common/services/pyautogui/image/edge_dom.png'

        if x is None and y is None:
            x, y = pyautogui.locateCenterOnScreen(image_path)
            x = x
            y = y - 40
        pyautogui.moveTo(x, y, duration=0.25)
        pyautogui.click()
        pyautogui.scroll(3500, x=x, y=y)
        sleep(0.5)
        self.click_icon(image_path, x=x, y=y, diff_y=30, type='right')
        sleep(0.2)

        pyautogui.moveTo(x + 50, y + 150)
        pyautogui.click()
        sleep(0.2)

        pyautogui.moveTo(x + 260, y + 150)
        pyautogui.click()

        return pyperclip.paste()

    def dummy_move(self, x, y, random_x=10, random_y=10):
        final_x = int(x + random.uniform(random_x, random_x * -1))
        final_y = int(y + random.uniform(random_y, random_y * -1))
        move1_x = int(final_x + random.uniform(100, 100 * -1))
        move1_y = int(final_y + random.uniform(100, 100 * -1))
        move2_x = int(final_x + random.uniform(50, 50 * -1))
        move2_y = int(final_y + random.uniform(50, 50 * -1))
        pyautogui.moveTo(move1_x, move1_y, duration=0.25)
        pyautogui.moveTo(move2_x, move2_y, duration=0.25)
        pyautogui.moveTo(final_x, final_y, duration=0.25)
        sleep(0.2)
        return final_x, final_y

    def dummy_scroll(self, x, y, random_x=10, random_y=10, scroll_to=300):
        final_x, final_y = self.dummy_move(x, y, random_x=random_x, random_y=random_y)
        pyautogui.click()
        sleep(0.3 * random.random())
        scroll1 = int((scroll_to * 0.3 + random.uniform(scroll_to * 0.3, 0)) * -1)
        scroll2 = int((scroll_to * 0.3 + random.uniform(scroll_to * 0.3, 0)) * -1)
        scroll3 = int((scroll_to * 0.3 + random.uniform(scroll_to * 0.3, 0)) * -1)
        random_x1 = x + random.uniform(random_x, random_x * -1)
        random_x2 = x + random.uniform(random_x, random_x * -1)

        pyautogui.scroll(scroll1, x=(final_x + random_x1), y=final_y)
        sleep(0.3 * random.random())
        pyautogui.scroll(scroll2, x=(final_x + random_x2), y=final_y)
        sleep(0.2 * random.random())
        pyautogui.scroll(scroll3, x=final_x, y=final_y)
        sleep(0.2 * random.random())
        return pyautogui.position()

    def test(self, x, y, random_x=10, random_y=10):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')

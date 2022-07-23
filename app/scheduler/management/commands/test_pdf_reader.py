import pdfminer
from pdfminer.high_level import extract_text
import sys, os
from pathlib import Path
from subprocess import call

from common.enums.status import Status

from common.services.components.system_exception import SystemException
from common.services.selenium_service import SeleniumService
from common.services.site.instagram_service import InstagramService

from scheduler.services.task_service import TaskService

from django.core.management.base import BaseCommand
from google.cloud import bigquery
from google.oauth2 import service_account





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

            dir_path = os.path.join(os.getcwd(), 'scheduler/pdf/output')

            records = []
            records.append(
                ",".join(['no', 'name', 'birth_day', 'birth_place', 'blood_type', 'special_skill', 'cf', 'height', 'bust', 'west',
                          'hip', 'shoe_size', 'head_circumference', 'around_the_neck', 'girder_length', 'sleeve_length',
                          'inseam', 'shoulder_width'])
            )

            for file_name in os.listdir(dir_path):
                print(file_name)
                file_path = os.path.join(dir_path, file_name)

                # ファイルをオープンする
                file_data = open(file_path, "r")

                no = file_name.replace('out', '').replace('.txt', '')
                name = ''
                is_birth_day = False
                birth_day = ''
                is_birth_place = False
                birth_place = ''
                blood_type = ''
                is_special_skill = False
                special_skill = ''
                is_cf = False
                cfs = []
                height = ''
                bust = ''
                west = ''
                hip = ''
                shoe_size = ''
                head_circumference = ''
                around_the_neck = ''
                girder_length = ''
                sleeve_length = ''
                inseam = ''
                shoulder_width = ''

                # 一行ずつ読み込んでは表示する
                for line in file_data:
                    print(line)
                    if name == '':
                        name = (line or '').strip()

                    if '【生年月日】' in line:
                        is_birth_day = True

                    if is_birth_day and '【生年月日】' not in line and birth_day == '':
                        birth_day = (line or '').strip().replace(' ', '　').split('　')[0]
                        birth_day = birth_day.replace('年', '/').replace('月', '/').replace('日生', '')
                        continue

                    if '【 出身地 】' in line:
                        is_birth_place = True

                    if is_birth_place and '【 出身地 】' not in line and birth_place == '':
                        birth_place = (line or '').strip()
                        continue

                    if blood_type == '':
                        candidate_blood_type = (line or '').strip()
                        if candidate_blood_type in ['Ａ', 'Ｂ', 'ＡＢ', 'Ｏ']:
                            blood_type = candidate_blood_type
                            continue

                    if '【　特技　】' in line or '【 特技 】' in line:
                        is_special_skill = True

                    if is_special_skill and ('【　特技　】' not in line and '【 特技 】' not in line) and special_skill == '':
                        special_skill = (line or '').strip()
                        if special_skill == '【 サイズ 】':
                            special_skill = ''

                    if '【ＣＦ】' in line:
                        is_cf = True

                    if is_cf and '【ＣＦ】' not in line:
                        candidate_cf = (line or '').strip()
                        if '･' in candidate_cf:
                            cfs.append(candidate_cf)

                    if '【 サイズ 】' in line:
                        is_birth_day = False
                        is_birth_place = False
                        is_special_skill = False
                        is_cf = False
                        continue

                    if '身　　長:' in line or '長:' in line:
                        height = ((line or '').split('長:')[1] or '').replace('cm', '').strip()
                        continue

                    if 'バ ス ト:' in line:
                        bust = ((line or '').split('バ ス ト:')[1] or '').replace('cm', '').strip()
                        continue

                    if 'ウエスト:' in line:
                        west = ((line or '').split('ウエスト:')[1] or '').replace('cm', '').strip()
                        continue

                    if 'ヒ ッ プ:' in line:
                        hip = ((line or '').split('ヒ ッ プ:')[1] or '').replace('cm', '').strip()
                        continue

                    if '靴サイズ:' in line:
                        shoe_size = ((line or '').split('靴サイズ:')[1] or '').replace('cm', '').strip()
                        continue

                    if '頭回り:' in line:
                        head_circumference = ((line or '').split('頭回り:')[1] or '').replace('cm', '').strip()
                        continue

                    if '首回り:' in line:
                        around_the_neck = ((line or '').split('首回り:')[1] or '').replace('cm', '').strip()
                        continue

                    if '桁　丈:' in line or '桁 丈:' in line:
                        girder_length = ((line or '').replace('桁 丈:', '桁　丈:').split('桁　丈:')[1] or '').replace('cm', '').strip()
                        continue

                    if '袖　丈:' in line or '袖 丈:' in line:
                        sleeve_length = ((line or '').replace('袖 丈:', '袖　丈:').split('袖　丈:')[1] or '').replace('cm', '').strip()
                        continue

                    if '股　下:' in line or '股 下:' in line:
                        inseam = ((line or '').replace('股 下:', '股　下:').split('股　下:')[1] or '').replace('cm', '').strip()
                        continue

                    if '肩　幅:' in line or '肩 幅:' in line:
                        shoulder_width = ((line or '').replace('肩 幅:', '肩　幅:').split('肩　幅:')[1] or '').replace('cm', '').strip()
                        continue

                records.append(
                    ",".join([no, name, birth_day, birth_place, blood_type, special_skill, ' / '.join(cfs), height, bust, west, hip, shoe_size,
                     head_circumference, around_the_neck, girder_length, sleeve_length, inseam,
                     shoulder_width])
                )

            # records.append("\n".join(record))

            csv_text = "\n".join(records)

            pdf_write_path = os.path.join(os.getcwd(), 'scheduler/pdf/out/extract.csv')

            with open(pdf_write_path, mode='w') as f:
                f.write(csv_text)



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

# pdfへの出力
def out_to_pdf():
    pdf_read_path = os.path.join(os.getcwd(), 'scheduler/pdf/プロフィール301-9999.pdf')

    for i in range(55):
        num = i + 1 + 300
        pdf_read_text = extract_text(pdf_read_path, page_numbers=[i])
        print(pdf_read_text)

        pdf_write_path = os.path.join(os.getcwd(), 'scheduler/pdf/out/out' + str(num) + '.txt')

        with open(pdf_write_path, mode='w') as f:
            f.write(pdf_read_text)

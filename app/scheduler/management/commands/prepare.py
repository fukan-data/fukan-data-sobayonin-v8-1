from google.cloud import bigquery
import os

from django.core.management.base import BaseCommand

from common.consts.instagram import INSTAGRAM
from common.services.google.big_query import BigQueryService
from scheduler.factories.task import TaskFactory
from scheduler.factories.task_option import TaskOptionFactory

big_query = BigQueryService()


class Command(BaseCommand):
    help = 'Making data of Task'

    def add_arguments(self, parser):
        parser.add_argument('-b', '--big-query', nargs='?', default='', type=str)
        parser.add_argument('-d', '--develop', action='store_true')
        parser.add_argument('-f', '--file', action='store_true')
        parser.add_argument('-s', '--sql', nargs='?', default='', type=str)

    def handle(self, *args, **options):
        if options['sql'] == 'task':
            print('Run making sql data for task')
            task = TaskFactory.create(task_service='system', task_name='RUN_GAS', task_category=0, task_status=0, max_time=15,
                               notification_emails='fukan.data.labo@gmail.com', notification_slack_url=0)
            TaskOptionFactory.create(task_id=task.task_id, url='https://script.google.com/macros/s/AKfycbzF_jYFm2COvM_CQcObwceWfVj8-M2EmM-epdE1S5u4eEqI_hL3lKUvzaMHNxzdGsej/exec')
            print('End making sql data')

        if options['file']:
            print('Run making file')
            os.makedirs(INSTAGRAM.PATH.DIR.STOCK, exist_ok=True)
            print('End making file')

        if options['big-query'] == 'instagram':
            table_id = "sobayonin-db.sobayonin_develop.instagram_page"
            schema = [
                bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            ]
            big_query.create_table(table_id, schema)

        elif options['big-query'] == 'connectfam':
            table_id = "sobayonin-db.sobayonin_develop.person"
            schema = [
                bigquery.SchemaField("local_pc", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("create_time", "DATETIME", mode="REQUIRED"),
                bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name_sei", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name_mei", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name_sei_kana", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name_mei_kana", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("tel", "STRING"),
                bigquery.SchemaField("address", "STRING"),
                bigquery.SchemaField("country", "STRING"),
                bigquery.SchemaField("face_photo_url", "STRING"),
                bigquery.SchemaField("birth_day", "DATE"),

            ]
            big_query.create_table(table_id, schema)


            table_id = "sobayonin-db.sobayonin_develop.action"
            schema = [
                bigquery.SchemaField("person", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("local_pc", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("create_time", "DATETIME", mode="REQUIRED"),
                bigquery.SchemaField("purpose", "STRING", mode="REQUIRED"),  # VISIT_PURPOSE, ACTIVITY_HISTORY, INSTAGRAM, TWITTER, YOUTUBE, TIKTOK, FACEBOOK, BLOG_HOMEPAGE, OTHERS
                bigquery.SchemaField("start", "DATETIME"),
                bigquery.SchemaField("end", "DATETIME"),
                bigquery.SchemaField("memo", "STRING"),  # ACTIVITY_HISTORY, OTHERS
                bigquery.SchemaField("url", "STRING"),  # INSTAGRAM, TWITTER, YOUTUBE, TIKTOK, FACEBOOK, BLOG_HOMEPAGE
                bigquery.SchemaField("followers", "INTEGER"),  # INSTAGRAM, TWITTER, TIKTOK, FACEBOOK
                bigquery.SchemaField("subscribers", "INTEGER"),  # YOUTUBE
                bigquery.SchemaField("calendar_id", "INTEGER"),

                bigquery.SchemaField("corresponding_person", "INTEGER"),  # 変更すべき複数の場合?

            ]
            big_query.create_table(table_id, schema)


            table_id = "sobayonin-db.sobayonin_develop.calendar"
            schema = [
                bigquery.SchemaField("calendar_id", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("meet_id", "STRING"),
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("description", "STRING"),
                bigquery.SchemaField("html_link", "STRING"),

            ]
            big_query.create_table(table_id, schema)








        self.stdout.write("Success: Making data of Task")

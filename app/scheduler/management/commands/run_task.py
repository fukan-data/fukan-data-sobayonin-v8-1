from scheduler.services.task_service import TaskService

from django.core.management.base import BaseCommand


service = TaskService()
logger = service.logger


class Command(BaseCommand):
    help = 'Task runner'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--develop', action='store_true')

    def handle(self, *args, **options):
        logger.info('Start: Task runner')

        if options['develop']:
            logger.info('Develop mode')

        while True:
            # リセットのため終了する
            if not service.is_working_time(14, 30, 14, 40):
                logger.info("batch_runner終了: リセット時刻のため")
                exit(0)

            try:
                # キューの呼び出し
                for task in service.get_tasks():
                    logger.info("Start task: [" + task.task.task_service + "]" + task.task.task_name)
                    print(task.task.reserve_start)
                    print(task.task.task_name, task.url)

                    # タスクの内容をタスクシートに転記する（対象となるタスクに限る）
                    service.regist_task_sheet(task)

                    exit(0)

                    # task_runnerによるタスクの実行（対象となるタスクに限る）
                    # ex) run_gas, calender_to_queue
                    service.run_task(task)

                    # queueの実行結果を更新
                    service.set_result()

                    # task_id = models.AutoField(verbose_name='タスクID', primary_key=True, blank=True)
                    # task_service = models.CharField(verbose_name='タスクサービス名', max_length=16)
                    # task_service_id = models.IntegerField(verbose_name='タスクサービスID')
                    # task_name = models.CharField(verbose_name='タスク名', max_length=64)
                    # task_category = models.IntegerField(verbose_name='タスクカテゴリー', choices=TaskCategory.choices())
                    # task_status = models.IntegerField(verbose_name='タスクステータス', choices=TaskStatus.choices())
                    # reserve_start = models.DateTimeField(verbose_name='予約開始日時', null=True, blank=True)
                    # run_start = models.DateTimeField(verbose_name='実行開始日時', null=True, blank=True)
                    # run_end = models.DateTimeField(verbose_name='実行終了日時', null=True, blank=True)
                    # max_time = models.IntegerField(verbose_name='実行最大時間（分）', null=True, blank=True)
                    # notification_emails = models.CharField(verbose_name='通知メール先', max_length=256, null=True, blank=True)
                    # notification_slack_url = models.CharField(verbose_name='通知スラック先', max_length=128, null=True, blank=True)
                    # task_message = models.CharField(verbose_name='タスクメッセージ', max_length=256, null=True, blank=True)

                exit(0)

                # タスクシートの内容をキューに反映する
                service.set_tasks_by_sheet()

            except Exception as e:
                # queueが失敗したことのシステムエラー
                # スクレーパーの失敗は、個別のタスクを動かすPCがmailを送信する

                print(e.__str__())

                exit(0)

                # queueの実行結果を更新
                service.set_result()

                # send slack and mail
                service.notify()

            print("eeeee 222")
            logger.info("eeeee 222")

            service.test()

            print("wwwww")
            # close
            exit(0)



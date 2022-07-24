import gspread
from common.enums.status import Status
from common.services.google_service import GoogleService
from google.cloud import bigquery


class BigQueryService(GoogleService):
    def __init__(self, logger=None, **kwargs):
        super().__init__(logger, **kwargs)
        self.gc = gspread.authorize(self.credentials)
        self.logger = self.get_logger() if logger is None else logger
        self.table = None
        self.sheet = None

    def run_query(self, sql):
        try:
            client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
            df = client.query(sql).to_dataframe()
            return Status.get_response(Status.SUCCESS, data=df)
        except Exception as e:
            return Status.get_response(Status.BIG_QUERY_ERROR, detail=e.__str__())

    def insert_rows(self, table_id, rows):
        try:
            client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
            errors = client.insert_rows_json(table_id, rows)  # Make an API request.
            if errors == []:
                return Status.get_response(Status.SUCCESS)
            else:
                return Status.get_response(Status.BIG_QUERY_ERROR, detail=errors)
        except Exception as e:
            return Status.get_response(Status.BIG_QUERY_ERROR, detail=e.__str__())

    def create_table(self, table_id, schema):
        try:
            client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
            table = bigquery.Table(table_id, schema=schema)
            table = client.create_table(table)  # Make an API request.
            return Status.get_response(Status.SUCCESS, data=table)
            # print(
            #     "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
            # )

        except Exception as e:
            return Status.get_response(Status.BIG_QUERY_ERROR, detail=e.__str__())

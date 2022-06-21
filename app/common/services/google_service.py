from common.services.common_service import CommonService
from google.oauth2 import service_account


class GoogleService(CommonService):
    def __init__(self, logger, **kwargs):
        super().__init__(**kwargs)
        key_path = "common/keys/sobayonin-db-5afdf912e5c7.json"
        self.credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=[
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/drive",
                "https://spreadsheets.google.com/feeds",
            ],
        )
        self.project_id = self.credentials.project_id

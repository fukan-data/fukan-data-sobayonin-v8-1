import gspread
from common.services.table_service import TableService
from common.enums.status import Status
from common.services.google_service import GoogleService


class SpreadSheetService(GoogleService):
    def __init__(self, logger, **kwargs):
        super().__init__(logger, **kwargs)
        self.gc = gspread.authorize(self.credentials)
        self.logger = self.get_logger() if logger is None else logger
        self.table = None
        self.sheet = None

    def open_spread_sheet(self, sheet_id):
        ss = self.gc.open_by_key(sheet_id)
        return {
            'id': sheet_id,
            'title': ss.title,
            'ss': ss
        }

    def get_values(self, sheet_id, sheet_name, sheet_range):
        spread_sheet = self.open_spread_sheet(sheet_id)
        try:
            values = spread_sheet['ss'].values_get(sheet_name + "!" + sheet_range)
            values.update(sheet_id=sheet_id, sheet_name=sheet_name, range=sheet_range, title=spread_sheet['title'])
            return Status.get_response(Status.SUCCESS, data=values)

        except Exception as e:
            self.logger.error('can not get values: ' + e.__str__())
            return Status.get_response(Status.GOOGLE_SPREAD_SHEET_ERROR)

    def set_values(self, sheet_id, sheet_name, sheet_range, values):
        spread_sheet = self.open_spread_sheet(sheet_id)
        try:
            sheet = spread_sheet['ss'].worksheet(sheet_name)
            sheet.update(sheet_range, values)
            return Status.get_response(Status.SUCCESS)

        except Exception as e:
            self.logger.error('can not set values: ' + e.__str__())
            return Status.get_response(Status.GOOGLE_SPREAD_SHEET_ERROR)

    def get_df_table(self, sheet_id, sheet_name, columns=None, where=None):
        spread_sheet = self.open_spread_sheet(sheet_id)
        values = spread_sheet['ss'].worksheet(sheet_name).get_all_values()
        return TableService(logger=self.logger)\
            .create_table(values=values)\
            .select(columns)\
            .filter(where)

    def append_row(self, sheet_id, sheet_name, row):
        spread_sheet = self.open_spread_sheet(sheet_id)
        spread_sheet['ss'].worksheet(sheet_name).append_row(row)

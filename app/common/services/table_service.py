import pandas as pd
from common.services.common_service import CommonService


# 2次元配列に特化した行列の整形
class TableService(CommonService):
    def __init__(self, logger, **kwargs):
        super().__init__(**kwargs)
        self.logger = logger

    def create_table(self, values=None, header=None, body=None):
        if not (values is None or (header is None and body is None)):
            raise Exception('illegal params')

        if values is not None:
            header = values[0]
            body = values[1:len(values)]
        if header is not None:
            header = header
        if body is not None:
            body = body

        self.table = pd.DataFrame(data=body, columns=header)
        return self

    # a == "NY", a != "AT", a < 3, a in ["NY", "TX"], a.str.contains("Y"), a.str.endswith("Y"), a.str.match(".*i.*e")
    def filter(self, where=None):
        if where is not None:
            self.table = self.table.query(where)
        return self

    def select(self, columns=None):
        if columns is not None:
            self.table = self.table[columns]
        return self

    def append(self, record):
        if record is not None:
            self.table = self.table.append(record, ignore_index=True)
        return self






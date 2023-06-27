import os.path

import pandas as pd
from rptgen.prepare.reader import Reader


class PadReader(Reader):
    def __init__(self, base_dir: str):
        super().__init__(base_dir=base_dir)

    def read(self, filename: str) -> pd.DataFrame:
        filepath = self.get_filepath(self.base_dir, filename)
        fn_reader = self.proxy(filepath)
        return fn_reader(filepath)

    def proxy(self, filepath: str):
        _, ext = os.path.splitext(filepath)
        if ext == '.xlsx':
            return self.from_excel
        if ext == '.parquet':
            return self.from_parquet

    def from_excel(self, filepath: str):
        return pd.read_excel(filepath)

    def from_parquet(self, filepath: str):
        return pd.read_parquet(filepath)
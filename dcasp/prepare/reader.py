import os.path

import pandas as pd
from typeguard import typechecked

from rptgen.prepare.reader import Reader


@typechecked
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

    @staticmethod
    def from_excel(filepath: str):
        return pd.read_excel(filepath)

    @staticmethod
    def from_parquet(filepath: str):
        return pd.read_parquet(filepath)

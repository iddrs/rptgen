import os
from abc import ABC, abstractmethod

import pandas as pd
from typeguard import typechecked


@typechecked
class Reader(ABC):

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    @abstractmethod
    def read(self, filename: str) -> pd.DataFrame:
        pass

    @staticmethod
    def get_filepath(base_dir, filename) -> str:
        return os.path.join(base_dir, filename)

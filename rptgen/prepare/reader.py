import pandas as pd
from abc import ABC, abstractmethod
import os
from typeguard import typechecked

@typechecked
class Reader(ABC):

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    @abstractmethod
    def read(self, filename: str) -> pd.DataFrame:
        pass

    def get_filepath(self, base_dir, filename) -> str:
        return os.path.join(base_dir, filename)
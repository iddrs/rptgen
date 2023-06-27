import pandas as pd
from typeguard import typechecked


@typechecked
class Frames:
    frames: dict[pd.DataFrame] = dict()
    index: int = 0

    def add_frame(self, name: str, df: pd.DataFrame):
        self.frames[name] = df
        return self

    def get_frame(self, name: str) -> pd.DataFrame:
        return self[name]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.frames):
            self.index = 0
            raise StopIteration
        frame = list(self.frames.values())[self.index]
        key = list(self.frames.keys())[self.index]
        self.index += 1
        return key, frame

    def names(self) -> list:
        return list(self.frames.keys())

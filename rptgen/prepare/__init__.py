import pandas as pd
from abc import ABC, abstractmethod
from rptgen.frame import Frames
from rptgen.escopo import Escopo
from typeguard import typechecked


@typechecked
class Prepare(ABC):

    def __init__(self, escopo: Escopo, **kwargs: pd.DataFrame):
        self.escopo = escopo
        self.frames = kwargs

    @abstractmethod
    def prepare(self) -> Frames:
        pass
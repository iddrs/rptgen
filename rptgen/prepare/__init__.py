from abc import ABC, abstractmethod

import pandas as pd
from typeguard import typechecked

from rptgen.escopo import Escopo
from rptgen.frame import Frames


@typechecked
class Prepare(ABC):

    def __init__(self, escopo: Escopo, **kwargs: pd.DataFrame):
        self.escopo = escopo
        self.frames = kwargs

    @abstractmethod
    def prepare(self) -> Frames:
        pass

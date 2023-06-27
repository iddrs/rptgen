from abc import ABC, abstractmethod
from rptgen.frame import Frames
import os

class Writer(ABC):

    def __init__(self, filepath: str):
        self.filepath = filepath
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    @abstractmethod
    def write(self, frames: Frames):
        pass
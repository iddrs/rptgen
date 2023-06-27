import os
import pandas as pd
from rptgen.frame import Frames
from rptgen.prepare.writer import Writer

class ExcelWriter(Writer):

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def write(self, frames: Frames):
        for framename, df in frames:
            df.to_excel(self.filepath, sheet_name=framename, index=None)
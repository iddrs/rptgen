from typeguard import typechecked

from rptgen.frame import Frames
from rptgen.prepare.writer import Writer


@typechecked
class ExcelWriter(Writer):
    """Classe para escrever DataFrames em arquivos Excel.

    Herda de
    ---------
    Writer

    Métodos
    -------
    write(frames: Frames)
        Escreve os frames em um arquivo Excel.
    """
    def __init__(self, filepath: str):
        """Inicializa o escritor com o caminho do arquivo especificado.

        Parâmetros
        ----------
        filepath : str
            Caminho do arquivo a ser escrito.
        """
        super().__init__(filepath=filepath)

    def write(self, frames: Frames):
        """Escreve os frames em um arquivo Excel.

        Parâmetros
        ----------
        frames : Frames
            Instância da classe Frames contendo os DataFrames a serem escritos.
        """
        for framename, df in frames:
            df.to_excel(self.filepath, sheet_name=framename, index=None)

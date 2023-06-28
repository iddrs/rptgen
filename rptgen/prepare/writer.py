import os
from abc import ABC, abstractmethod

from typeguard import typechecked

from rptgen.frame import Frames


@typechecked
class WriterBase(ABC):
    """Classe abstrata base para escritores de arquivos.

    Atributos
    ---------
    filepath : str
        Caminho do arquivo a ser escrito.

    Métodos
    -------
    write(frames: Frames)
        Método abstrato para escrever os frames no arquivo.
    """
    def __init__(self, filepath: str):
        """Inicializa o escritor com o caminho do arquivo especificado.

        Parâmetros
        ----------
        filepath : str
            Caminho do arquivo a ser escrito.
        """
        self.filepath = filepath
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    @abstractmethod
    def write(self, frames: Frames):
        """Método abstrato para escrever os frames no arquivo.

        Parâmetros
        ----------
        frames : Frames
            Instância da classe Frames contendo os DataFrames a serem escritos.

        Exceções
        --------
        NotImplementedError
            Levantada quando o método não é implementado pela subclasse.
        """

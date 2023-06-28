from abc import ABC, abstractmethod

import pandas as pd
from typeguard import typechecked

from rptgen.escopo import Escopo
from rptgen.frame import Frames


@typechecked
class PrepareBase(ABC):
    """Classe abstrata base para preparação de dados.

    Atributos
    ---------
    escopo : Escopo
        Escopo dos dados a serem preparados.
    frames : dict[str, pd.DataFrame]
        Dicionário contendo os DataFrames com os dados a serem preparados.

    Métodos
    -------
    prepare() -> Frames
        Método abstrato para preparar os dados e retornar uma instância da classe Frames.
    """
    def __init__(self, escopo: Escopo, **kwargs: pd.DataFrame):
        """Inicializa o preparador com o escopo e os DataFrames especificados.

        Parâmetros
        ----------
        escopo : Escopo
            Escopo dos dados a serem preparados.
        kwargs : pd.DataFrame
            Dicionário contendo os DataFrames com os dados a serem preparados.
        """
        self.escopo = escopo
        self.frames = kwargs

    @abstractmethod
    def prepare(self) -> Frames:
        """Método abstrato para preparar os dados e retornar uma instância da classe Frames.

        Retorno
        -------
        Frames
            Instância da classe Frames contendo os DataFrames com os dados preparados.

        Exceções
        --------
        NotImplementedError
            Levantada quando o método não é implementado pela subclasse.
        """

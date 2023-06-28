import os
from abc import ABC, abstractmethod

import pandas as pd
from typeguard import typechecked


@typechecked
class ReaderBase(ABC):
    """Classe abstrata base para leitores de arquivos.

    Atributos
    ---------
    base_dir : str
        Diretório base para os arquivos a serem lidos.

    Métodos
    -------
    read(filename: str) -> pd.DataFrame
        Método abstrato para ler um arquivo e retornar um DataFrame.
    get_filepath(base_dir: str, filename: str) -> str
        Retorna o caminho completo do arquivo com base no diretório base e no nome do arquivo.
    """
    def __init__(self, base_dir: str):
        """Inicializa o leitor com o diretório base especificado.

        Parâmetros
        ----------
        base_dir : str
            Diretório base para os arquivos a serem lidos.
        """
        self.base_dir = base_dir

    @abstractmethod
    def read(self, filename: str) -> pd.DataFrame:
        """Método abstrato para ler um arquivo e retornar um DataFrame.

        Parâmetros
        ----------
        filename : str
            Nome do arquivo a ser lido.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo os dados lidos do arquivo.

        Exceções
        --------
        NotImplementedError
            Levantada quando o método não é implementado pela subclasse.
        """
        pass

    @staticmethod
    def get_filepath(base_dir, filename) -> str:
        """Retorna o caminho completo do arquivo com base no diretório base e no nome do arquivo.

        Parâmetros
        ----------
        base_dir : str
            Diretório base para os arquivos a serem lidos.
        filename : str
            Nome do arquivo a ser lido.

        Retorno
        -------
        str
            String com o caminho completo para o arquivo.
        """
        return os.path.join(base_dir, filename)

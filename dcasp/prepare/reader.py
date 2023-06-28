import os.path

import pandas as pd
from typeguard import typechecked

from rptgen.prepare.reader import ReaderBase


@typechecked
class PadReader(ReaderBase):
    """Classe para ler arquivos PAD.

    Herda de
    ---------
    ReaderBase

    Métodos
    -------
    read(filename: str) -> pd.DataFrame
        Lê um arquivo e retorna um DataFrame.
    proxy(filepath: str) -> callable
        Retorna a função apropriada para ler o arquivo com base na extensão do arquivo.
    from_excel(filepath: str) -> pd.DataFrame
        Lê um arquivo Excel e retorna um DataFrame.
    from_parquet(filepath: str) -> pd.DataFrame
        Lê um arquivo Parquet e retorna um DataFrame.
    """
    def __init__(self, base_dir: str):
        """Inicializa o leitor com o diretório base especificado.

        Parâmetros
        ----------
        base_dir : str
            Diretório base para os arquivos a serem lidos.
        """
        super().__init__(base_dir=base_dir)

    def read(self, filename: str) -> pd.DataFrame:
        """Lê um arquivo e retorna um DataFrame.

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
        ValueError
            Levantada quando a extensão do arquivo não é reconhecida.
        """
        filepath = self.get_filepath(self.base_dir, filename)
        fn_reader = self.proxy(filepath)
        return fn_reader(filepath)

    def proxy(self, filepath: str) -> callable:
        """Retorna a função apropriada para ler o arquivo com base na extensão do arquivo.

        Parâmetros
        ----------
        filepath : str
            Caminho completo do arquivo a ser lido.

        Retorno
        -------
        callable
            Função apropriada para ler o arquivo com base na extensão do arquivo.

        Exceções
        --------
        ValueError
            Levantada quando a extensão do arquivo não é reconhecida.
        """
        _, ext = os.path.splitext(filepath)
        if ext == '.xlsx':
            return self.from_excel
        if ext == '.parquet':
            return self.from_parquet

    @staticmethod
    def from_excel(filepath: str):
        """Lê um arquivo Excel e retorna um DataFrame.

        Parâmetros
        ----------
        filepath : str
            Caminho completo do arquivo Excel a ser lido.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo os dados lidos do arquivo Excel.
        """
        return pd.read_excel(filepath)

    @staticmethod
    def from_parquet(filepath: str):
        """Lê um arquivo Parquet e retorna um DataFrame.

        Parâmetros
        ----------
        filepath : str
            Caminho completo do arquivo Parquet a ser lido.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo os dados lidos do arquivo Parquet.
        """
        return pd.read_parquet(filepath)

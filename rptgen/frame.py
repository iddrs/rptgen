import pandas as pd
from typeguard import typechecked


@typechecked
class Frames:
    """Classe para armazenar e gerenciar DataFrames.

    Cada DataFrame representa uma planilha em uma pasta de trabalho.

    Atributos
    ---------
    frames : dict[str, pd.DataFrame]
        Dicionário que armazena os DataFrames com seus respectivos nomes.
    index : int
        Índice usado para iterar sobre os DataFrames armazenados.

    Métodos
    -------
    add_frame(name: str, df: pd.DataFrame)
        Adiciona um DataFrame ao dicionário de frames com o nome especificado.
    get_frame(name: str) -> pd.DataFrame
        Retorna o DataFrame armazenado com o nome especificado.
    names() -> list
        Retorna uma lista com os nomes dos DataFrames armazenados.
    """
    frames: dict[str, pd.DataFrame] = dict()
    index: int = 0

    def add_frame(self, name: str, df: pd.DataFrame):
        """Adiciona um DataFrame ao dicionário de frames com o nome especificado.

        Parâmetros
        ----------
        name : str
            Nome do DataFrame a ser adicionado.
        df : pd.DataFrame
            DataFrame a ser adicionado.

        Retorno
        -------
        Frames
            Retorna a própria instância da classe para permitir encadeamento de métodos.
        """
        self.frames[name] = df
        return self

    def get_frame(self, name: str) -> pd.DataFrame:
        """Retorna o DataFrame armazenado com o nome especificado.

        Parâmetros
        ----------
        name : str
            Nome do DataFrame a ser retornado.

        Retorno
        -------
        pd.DataFrame
            DataFrame armazenado com o nome especificado.
        """
        return self[name]

    def __iter__(self):
        """Retorna a própria instância da classe como um iterador.

        Retorno
        -------
        Frames
            Instância da classe como um iterador.
        """
        return self

    def __next__(self):
        """Retorna o próximo par (nome, DataFrame) na iteração sobre os DataFrames armazenados.

        Retorno
        -------
        tuple[str, pd.DataFrame]
            Próximo par (nome, DataFrame) na iteração sobre os DataFrames armazenados.

        Exceções
        --------
        StopIteration
            Levantada quando todos os DataFrames já foram iterados.
        """
        if self.index >= len(self.frames):
            self.index = 0
            raise StopIteration
        frame = list(self.frames.values())[self.index]
        key = list(self.frames.keys())[self.index]
        self.index += 1
        return key, frame

    def names(self) -> list:
        """Retorna uma lista com os nomes dos DataFrames armazenados.

        Retorno
        -------
        list[str]
            Lista com os nomes dos DataFrames armazenados.
        """
        return list(self.frames.keys())

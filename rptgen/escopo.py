from enum import Enum

from typeguard import typechecked


@typechecked
class Escopo(Enum):
    """Classe de enumeração para representar os escopos de entidades.

    Atributos
    ---------
    PM : str
        Escopo para Prefeitura Municipal.
    RPPS : str
        Escopo para Regime Próprio de Previdência Social.
    FPSM : str
        Escopo para Fundo de Previdência Social do Município.
    CM : str
        Escopo para Câmara Municipal.
    MUN : str
        Escopo para Município.
    LEG : str
        Escopo para Legislativo.
    EXEC : str
        Escopo para Executivo.

    Métodos
    -------
    names() -> list[str]
        Retorna uma lista com os nomes dos escopos.
    get_entidade() -> list[str]
        Retorna uma lista com as entidades correspondentes ao escopo.
    """
    PM = 'pm'
    RPPS = 'fpsm'
    FPSM = RPPS
    CM = 'cm'
    MUN = 'mun'
    LEG = CM
    EXEC = 'exec'

    @classmethod
    def names(cls) -> list[str]:
        """Retorna uma lista com os nomes dos escopos.

        Retorno
        -------
        list[str]
            Lista com os nomes dos escopos.
        """
        return ['pm', 'fpsm', 'cm', 'mun', 'leg', 'exec']

    def __str__(self):
        """Retorna a representação em string do escopo.

        Retorno
        -------
        str
            Representação em string do escopo.
        """
        return f'{self.value}'

    def get_entidade(self):
        """Retorna uma lista com as entidades correspondentes ao escopo.

        Retorno
        -------
        list[str]
            Lista com as entidades correspondentes ao escopo.

        Exceções
        --------
        ValueError
            Levantada quando o valor do escopo não é reconhecido.
        """
        if self.value == 'pm':
            return ['pm']
        if self.value == 'cm':
            return ['cm']
        if self.value == 'mun':
            return ['pm', 'cm', 'fpsm']
        if self.value == 'rpps':
            return ['fpsm']
        if self.value == 'fpsm':
            return ['fpsm']
        if self.value == 'leg':
            return ['cm']
        if self.value == 'exec':
            return ['pm', 'fpsm']

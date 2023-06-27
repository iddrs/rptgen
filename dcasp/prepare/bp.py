import pandas as pd
from typeguard import typechecked

from rptgen.escopo import Escopo
from rptgen.frame import Frames
from rptgen.prepare import Prepare


@typechecked
class Prepare(Prepare):
    """Classe para preparação de dados.

    Herda de
    ---------
    Prepare

    Métodos
    -------
    prepare() -> Frames
        Prepara os dados e retorna uma instância da classe Frames.
    preprocess_bverenc(df: pd.DataFrame, escopo: Escopo) -> pd.DataFrame
        Pré-processa o DataFrame de bverenc com base no escopo especificado.
    quadro_principal(bverenc: pd.DataFrame) -> pd.DataFrame
        Gera o quadro principal com base no DataFrame de bverenc.
    calcula_colunas(linha: dict, df: pd.DataFrame, bverenc: pd.DataFrame) -> pd.DataFrame
        Calcula as colunas do quadro principal com base na linha especificada.
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
        super().__init__(escopo=escopo, **kwargs)

    def prepare(self) -> Frames:
        """Prepara os dados e retorna uma instância da classe Frames.

        Retorno
        -------
        Frames
            Instância da classe Frames contendo os DataFrames com os dados preparados.
        """
        df = self.frames['bverenc']
        df = self.preprocess_bverenc(df, self.escopo)

        frames = Frames()
        frames.add_frame('QuadroPrincipal', self.quadro_principal(df))
        return frames

    def preprocess_bverenc(self, df: pd.DataFrame, escopo: Escopo) -> pd.DataFrame:
        """Pré-processa o DataFrame de bverenc com base no escopo especificado.

        Parâmetros
        ----------
        df : pd.DataFrame
            DataFrame de bverenc a ser pré-processado.
        escopo : Escopo
            Escopo dos dados a serem pré-processados.

        Retorno
        -------
        pd.DataFrame
            DataFrame de bverenc pré-processado.
        """
        entidades = self.escopo.get_entidade()
        df = df[df['entidade'].isin(entidades)]
        df = df.query('escrituracao == "S"')
        return df

    def quadro_principal(self, bverenc: pd.DataFrame) -> pd.DataFrame:
        """Gera o quadro principal com base no DataFrame de bverenc.

        Parâmetros
        ----------
        bverenc : pd.DataFrame
            DataFrame de bverenc a ser usado para gerar o quadro principal.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo o quadro principal.
        """
        df = pd.DataFrame(columns=['Linha', 'ExercicioAtual', 'ExercicioAnterior'])
        linhas = [{'AtivoTotal': (bverenc['conta_contabil'].str.startswith('1'))},
                  {'AtivoCirculante': (bverenc['conta_contabil'].str.startswith('11'))},
                  {'AtivoCaixaEEquivalentesDeCaixa': (bverenc['conta_contabil'].str.startswith('111'))},
                  {'CreditosACurtoPrazo': (bverenc['conta_contabil'].str.startswith(('112', '113')))}
                  ]

        for i in linhas:
            df = pd.concat([df, self.calcula_colunas(i, df, bverenc)])
        return df

    def calcula_colunas(self, linha: dict, df: pd.DataFrame, bverenc: pd.DataFrame) -> pd.DataFrame:
        """Calcula as colunas do quadro principal com base na linha especificada.

        Parâmetros
        ----------
        linha : dict
            Dicionário contendo a linha e o filtro a serem usados para calcular as colunas.
        df : pd.DataFrame
            DataFrame contendo o quadro principal.
        bverenc : pd.DataFrame
            DataFrame de bverenc a ser usado para calcular as colunas.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo a linha calculada do quadro principal.
        """
        for idlinha, filtro in linha.items():
            df = bverenc[filtro][['saldo_final', 'saldo_inicial']]
            vlatual = df['saldo_inicial'].sum()
            vlanterior = df['saldo_final'].sum()
            return pd.DataFrame([{'Linha': idlinha, 'ExercicioAtual': vlatual, 'ExercicioAnterior': vlanterior}])

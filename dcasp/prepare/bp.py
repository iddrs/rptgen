import pandas as pd
from typeguard import typechecked

from rptgen.escopo import Escopo
from rptgen.frame import Frames
from rptgen.prepare import Prepare


@typechecked
class Prepare(Prepare):

    def __init__(self, escopo: Escopo, **kwargs: pd.DataFrame):
        super().__init__(escopo=escopo, **kwargs)

    def prepare(self) -> Frames:
        df = self.frames['bverenc']
        df = self.preprocess_bverenc(df, self.escopo)

        frames = Frames()
        frames.add_frame('QuadroPrincipal', self.quadro_principal(df))
        return frames

    def preprocess_bverenc(self, df: pd.DataFrame, escopo: Escopo) -> pd.DataFrame:
        entidades = self.escopo.get_entidade()
        df = df[df['entidade'].isin(entidades)]
        df = df.query('escrituracao == "S"')
        return df

    def quadro_principal(self, bverenc: pd.DataFrame) -> pd.DataFrame:
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
        for idlinha, filtro in linha.items():
            df = bverenc[filtro][['saldo_final', 'saldo_inicial']]
            vlatual = df['saldo_inicial'].sum()
            vlanterior = df['saldo_final'].sum()
            return pd.DataFrame([{'Linha': idlinha, 'ExercicioAtual': vlatual, 'ExercicioAnterior': vlanterior}])

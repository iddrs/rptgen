import pandas as pd
from typeguard import typechecked

from rptgen.escopo import Escopo
from rptgen.frame import Frames
from rptgen.prepare import Prepare


@typechecked
class BalancoPatrimonialPrepare(Prepare):
    """Classe para preparação de dados.

    Herda de
    ---------
    BalancoPatrimonialPrepare

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
        bverenc = self.frames['bverenc']
        bverenc = self.preprocess_bverenc(bverenc, self.escopo)

        frames = Frames()
        frames.add_frame('QuadroPrincipal', self.quadro_principal(bverenc))
        frames.add_frame('QuadroFinanceiroPermanente', self.quadro_financeiro(bverenc))
        frames.add_frame('QuadroCompensacao', self.quadro_compensacao(bverenc))
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
        linhas = [{'Ativo': (bverenc['conta_contabil'].str.startswith('1'))},
                  {'AtivoCirculante': (bverenc['conta_contabil'].str.startswith('11'))},
                  {'AtivoCaixaEEquivalentesDeCaixa': (bverenc['conta_contabil'].str.startswith('111'))},
                  {'CreditosACurtoPrazo': (bverenc['conta_contabil'].str.startswith(('112', '113')))},
                  {'InvestimentosEAplicacoesTemporariasACurtoPrazo': (bverenc['conta_contabil'].str.startswith('114'))},
                  {'Estoques': (bverenc['conta_contabil'].str.startswith('115'))},
                  {'AtivoNaoCirculanteMantidoParaVenda': (bverenc['conta_contabil'].str.startswith('116'))},
                  {'VPDPagasAntecipadamente': (bverenc['conta_contabil'].str.startswith('119'))},
                  {'AtivoNaoCirculante': (bverenc['conta_contabil'].str.startswith('12'))},
                  {'RealizavelALongoPrazo': (bverenc['conta_contabil'].str.startswith('121'))},
                  {'Investimentos': (bverenc['conta_contabil'].str.startswith('122'))},
                  {'Imobilizado': (bverenc['conta_contabil'].str.startswith('123'))},
                  {'Intangivel': (bverenc['conta_contabil'].str.startswith('124'))},
                  {'Diferido': (bverenc['conta_contabil'].str.startswith('125'))},
                  {'PassivoEPatrimonioLiquido': (bverenc['conta_contabil'].str.startswith('2'))},
                  {'PassivoCirculante': (bverenc['conta_contabil'].str.startswith('21'))},
                  {'ObrigacoesTrabalhistasPrevidenciariasEAssistenciaisAPagarACurtoPrazo': (
                      bverenc['conta_contabil'].str.startswith('211'))},
                  {'EmprestimosEFinanciamentosACurtoPrazo': (bverenc['conta_contabil'].str.startswith('212'))},
                  {'FornecedoresEContasAPagarACurtoPrazo': (bverenc['conta_contabil'].str.startswith('213'))},
                  {'ObrigacoesFiscaisACurtoPrazo': (bverenc['conta_contabil'].str.startswith('214'))},
                  {'ObrigacoesDeReparticoesAOutrosEntes': (bverenc['conta_contabil'].str.startswith('215'))},
                  {'ProvisoesACurtoPrazo': (bverenc['conta_contabil'].str.startswith('217'))},
                  {'DemaisObrigacoesACurtoPrazo': (bverenc['conta_contabil'].str.startswith('218'))},
                  {'PassivoNaoCirculante': (bverenc['conta_contabil'].str.startswith('22'))},
                  {'ObrigacoesTrabalhistasPrevidenciariasEAssistenciaisAPagarALongoPrazo': (
                      bverenc['conta_contabil'].str.startswith('221'))},
                  {'EmprestimosEFinanciamentosALongoPrazo': (bverenc['conta_contabil'].str.startswith('222'))},
                  {'FornecedoresEContasAPagarALongoPrazo': (bverenc['conta_contabil'].str.startswith('223'))},
                  {'ObrigacoesFiscaisALongoPrazo': (bverenc['conta_contabil'].str.startswith('224'))},
                  {'ProvisoesALongoPrazo': (bverenc['conta_contabil'].str.startswith('227'))},
                  {'DemaisObrigacoesALongoPrazo': (bverenc['conta_contabil'].str.startswith('228'))},
                  {'ResultadoDiferido': (bverenc['conta_contabil'].str.startswith('229'))},
                  {'PatrimonioLiquido': (bverenc['conta_contabil'].str.startswith('23'))},
                  {'PatrimonioSocialECapitalSocial': (bverenc['conta_contabil'].str.startswith('231'))},
                  {'AdiantamentoParaFuturoAumentoDeCapital': (bverenc['conta_contabil'].str.startswith('232'))},
                  {'ReservasDeCapital': (bverenc['conta_contabil'].str.startswith('233'))},
                  {'AjustesDeAvaliacaoPatrimonial': (bverenc['conta_contabil'].str.startswith('234'))},
                  {'ReservasDeLucros': (bverenc['conta_contabil'].str.startswith('235'))},
                  {'DemaisReservas': (bverenc['conta_contabil'].str.startswith('236'))},
                  {'ResultadosAcumulados': (bverenc['conta_contabil'].str.startswith('237'))},
                  {'AcoesCotasEmTesouraria': (bverenc['conta_contabil'].str.startswith('239'))}
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

    def quadro_financeiro(self, bverenc: pd.DataFrame) -> pd.DataFrame:
        """Cria um quadro financeiro com base em um DataFrame de entrada.

        Parâmetros
        ----------
        bverenc : pd.DataFrame
            DataFrame contendo informações financeiras.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo o quadro financeiro.
        """
        df = pd.DataFrame(columns=['Linha', 'ExercicioAtual', 'ExercicioAnterior'])
        linhas = [{'Ativo': (bverenc['conta_contabil'].str.startswith('1'))},
                  {'AtivoFinanceiro': (bverenc['conta_contabil'].str.startswith('1')) & (
                              bverenc['indicador_superavit_financeiro'] == 'F')},
                  {'AtivoPermanente': (bverenc['conta_contabil'].str.startswith('1')) & (
                          bverenc['indicador_superavit_financeiro'] == 'P')},
                  {'Passivo': (bverenc['conta_contabil'].str.startswith(('21', '22')))},
                  {'PassivoFinanceiro': ((bverenc['conta_contabil'].str.startswith(('21', '22'))) & (
                          bverenc['indicador_superavit_financeiro'] == 'F') | bverenc['conta_contabil'].str.startswith(('6221301', '6221305', '6311', '6315')))},
                  {'PassivoPermanente': (bverenc['conta_contabil'].str.startswith(('21', '22'))) & (
                          bverenc['indicador_superavit_financeiro'] == 'P')}
                  ]

        for i in linhas:
            df = pd.concat([df, self.calcula_colunas(i, df, bverenc)])

        df = pd.concat([df, self.calcula_saldo_patrimonial(bverenc)])
        return df

    def calcula_saldo_patrimonial(self, bverenc: pd.DataFrame) -> pd.DataFrame:
        """Calcula o saldo patrimonial com base em um DataFrame de entrada.

        Parâmetros
        ----------
        bverenc : pd.DataFrame
            DataFrame contendo informações financeiras.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo o saldo patrimonial calculado.
        """
        ativo = bverenc[bverenc['conta_contabil'].str.startswith('1')][['saldo_inicial', 'saldo_final']].sum()
        passivo = bverenc[bverenc['conta_contabil'].str.startswith(('21', '22'))][['saldo_inicial', 'saldo_final']].sum()
        vlatual = ativo['saldo_final'] - passivo['saldo_final']
        vlanterior = ativo['saldo_inicial'] - passivo['saldo_inicial']
        df = pd.DataFrame([{
            'Linha': 'SaldoPatrimonial',
            'ExercicioAtual': vlatual,
            'ExercicioAnterior': vlanterior,
        }])
        return df

    def quadro_compensacao(self, bverenc: pd.DataFrame) -> pd.DataFrame:
        """Cria um quadro de compensação com base em um DataFrame de entrada.

        Parâmetros
        ----------
        bverenc : pd.DataFrame
            DataFrame contendo informações financeiras.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo o quadro de compensação.
        """
        df = pd.DataFrame(columns=['Linha', 'ExercicioAtual', 'ExercicioAnterior'])
        linhas = [{'AtosPotenciaisAtivos': (bverenc['conta_contabil'].str.startswith('811'))},
                  {'GarantiasEContragarantiasRecebidas': (bverenc['conta_contabil'].str.startswith('8111'))},
                  {'DireitosConveniadosEOutrosInstrumentosCongeneres': (bverenc['conta_contabil'].str.startswith('8112'))},
                  {'DireitosContratuais': (bverenc['conta_contabil'].str.startswith('8113'))},
                  {'OutrosAtosPotenciaisAtivos': (bverenc['conta_contabil'].str.startswith('8119'))},
                  {'AtosPotenciaisPassivos': (bverenc['conta_contabil'].str.startswith('812'))},
                  {'GarantiasEContragarantiasConcedidas': (bverenc['conta_contabil'].str.startswith('8121'))},
                  {'ObrigacoesConveniadasEOutrosInstrumentosCongeneres': (
                      bverenc['conta_contabil'].str.startswith('8122'))},
                  {'ObrigacoesContratuais': (bverenc['conta_contabil'].str.startswith('8123'))},
                  {'OutrosAtosPotenciaisPassivos': (bverenc['conta_contabil'].str.startswith('8129'))},
                  ]
        for i in linhas:
            df = pd.concat([df, self.calcula_colunas(i, df, bverenc)])
        return df
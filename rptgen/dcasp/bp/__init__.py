from enum import Enum
from os import path, makedirs
import pandas as pd

class Escopo(Enum):
    CM = 0
    FPSM = 1
    PM = 2
    MUN = 3

class ETL():

    output_file = 'bp.xlsx'

    def __init__(self, config, ano, mes, escopo):
        self.ano = ano
        self.mes = mes
        self.escopo = escopo
        self.config = config

    def run(self):
        self.extract()
        self.transform()
        self.load()

    def extract(self):
        self.extract_bverenc()

    def extract_bverenc(self):
        source = path.join(self.config['pad']['base_dir'], f'{str(self.ano)}-{str(self.mes).zfill(2)}', 'excel', 'BVER_ENC.xlsx')
        self.bverenc = pd.read_excel(source, sheet_name='BVER_ENC')


    def transform(self):
        self.filtra_escopo()
        self.remove_sinteticas()

    def remove_sinteticas(self):
        self.bverenc = self.bverenc[self.bverenc['escrituracao'] == 'S'].copy()

    def filtra_escopo(self):
        if self.escopo == Escopo.PM:
            self.bverenc = self.bverenc[self.bverenc['entidade'] == 'pm'].copy()
        elif self.escopo == Escopo.FPSM:
            self.bverenc = self.bverenc[self.bverenc['entidade'] == 'fpsm'].copy()
        elif self.escopo == Escopo.CM:
            self.bverenc = self.bverenc[self.bverenc['entidade'] == 'cm'].copy()
        elif self.escopo == Escopo.MUN:
            self.bverenc = self.bverenc[
                self.bverenc['conta_contabil'].str.startswith(('11', '12', '21', '22', '3', '4'))
                & (self.bverenc['conta_contabil'].str[4] != '2')
            ].copy()

    def load(self):
        self.load_quadro_principal()

    def load_ano_anterior(self, frame):
        ano_anterior = self.ano - 1
        if self.escopo == Escopo.PM:
            escopo = 'pm'
        elif self.escopo == Escopo.FPSM:
            escopo = 'fpsm'
        elif self.escopo == Escopo.CM:
            escopo = 'cm'
        elif self.escopo == Escopo.MUN:
            escopo = 'mun'
        input = path.join(self.config['rptgen']['output_base_dir'], str(ano_anterior), str(self.mes).zfill(2), 'DCASP',
                           escopo, self.output_file)
        return pd.read_excel(input, sheet_name=frame)


    def save(self, df, frame):
        if self.escopo == Escopo.PM:
            escopo = 'pm'
        elif self.escopo == Escopo.FPSM:
            escopo = 'fpsm'
        elif self.escopo == Escopo.CM:
            escopo = 'cm'
        elif self.escopo == Escopo.MUN:
            escopo = 'mun'
        output = path.join(self.config['rptgen']['output_base_dir'], str(self.ano), str(self.mes).zfill(2), 'DCASP', escopo, self.output_file)

        if not path.isfile(path.dirname(output)):
            makedirs(path.dirname(output), exist_ok=True)
        df.to_excel(output, sheet_name=frame, index=False)

    def sum(self, df, col, filter):
        return round(df[filter][col].sum(), 2)

    def load_quadro_principal(self):
        frame = 'QuadroPrincipal'
        bverenc = self.bverenc
        df = pd.DataFrame(columns=['Linha', 'ExercicioAtual'])

        '''Ativo circulante'''
        r = pd.DataFrame([{
            'Linha': 'AtivoCirculante',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final', bverenc['conta_contabil'].astype(str).str.startswith('11'))
        }])
        df = pd.concat([df, r])

        '''Caixa e equivalentes de caixa'''
        r = pd.DataFrame([{
            'Linha': 'CaixaEEquivalentesDeCaixa',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('111'))
        }])
        df = pd.concat([df, r])

        '''Créditos a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'CreditosACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith(('112', '113')))
        }])
        df = pd.concat([df, r])

        '''Investimentos e aplicações temporárias a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'InvestimentosEAplicacoesTemporariasACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('114'))
        }])
        df = pd.concat([df, r])

        '''Estoques'''
        r = pd.DataFrame([{
            'Linha': 'Estoques',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('115'))
        }])
        df = pd.concat([df, r])

        '''Ativo não circulante mantido para venda'''
        r = pd.DataFrame([{
            'Linha': 'AtivoNaoCirculanteMantidoParaVenda',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('116'))
        }])
        df = pd.concat([df, r])

        '''VPD pagas antecipadamente'''
        r = pd.DataFrame([{
            'Linha': 'VPDPagasAntecipadamente',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('119'))
        }])
        df = pd.concat([df, r])

        '''Ativo não circulante'''
        r = pd.DataFrame([{
            'Linha': 'AtivoNaoCirculante',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('12'))
        }])
        df = pd.concat([df, r])

        '''Realizável a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'RealizavelALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('121'))
        }])
        df = pd.concat([df, r])

        '''Investimentos'''
        r = pd.DataFrame([{
            'Linha': 'Investimentos',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('122'))
        }])
        df = pd.concat([df, r])

        '''Imobilizado'''
        r = pd.DataFrame([{
            'Linha': 'Imobilizado',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('123'))
        }])
        df = pd.concat([df, r])

        '''Intangível'''
        r = pd.DataFrame([{
            'Linha': 'Intangivel',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('124'))
        }])
        df = pd.concat([df, r])

        '''Ativo Diferido'''
        r = pd.DataFrame([{
            'Linha': 'AtivoDiferido',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('125'))
        }])
        df = pd.concat([df, r])

        '''Ativo Total'''
        r = pd.DataFrame([{
            'Linha': 'AtivoTotal',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('1'))
        }])
        df = pd.concat([df, r])

        '''Passivo circulante'''
        r = pd.DataFrame([{
            'Linha': 'PassivoCirculante',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('21'))
        }])
        df = pd.concat([df, r])

        '''Obrigações trabalhistas, previdenciárias e assistencias a pagar a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'ObrigacoesTrabalhistasPrevidenciariasEAssistenciaisAPagarACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('211'))
        }])
        df = pd.concat([df, r])

        '''Empréstimos e financiamentos a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'EmprestimosEFinanciamentosACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('212'))
        }])
        df = pd.concat([df, r])

        '''Fornecedores e contas a pagar a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'FornecedoresEContasAPagarACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('213'))
        }])
        df = pd.concat([df, r])

        '''Obrigações fiscais a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'ObrigacoesFiscaisACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('214'))
        }])
        df = pd.concat([df, r])

        '''Obrigações de repartições a outros entes'''
        r = pd.DataFrame([{
            'Linha': 'ObrigacoesDeReparticoesAOutrosEntes',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('215'))
        }])
        df = pd.concat([df, r])

        '''Provisões a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'ProvisoesACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('217'))
        }])
        df = pd.concat([df, r])

        '''Demais obrigações a curto prazo'''
        r = pd.DataFrame([{
            'Linha': 'DemaisObrigacoesACurtoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('218'))
        }])
        df = pd.concat([df, r])

        '''Passivo não circulante'''
        r = pd.DataFrame([{
            'Linha': 'PassivoNaoCirculante',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('22'))
        }])
        df = pd.concat([df, r])

        '''Obrigações trabalhistas, previdenciárias e assistencias a pagar a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'ObrigacoesTrabalhistasPrevidenciariasEAssistenciaisAPagarALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('221'))
        }])
        df = pd.concat([df, r])

        '''Empréstimos e financiamentos a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'EmprestimosEFinanciamentosALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('222'))
        }])
        df = pd.concat([df, r])

        '''Fornecedores e contas a pagar a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'FornecedoresEContasAPagarALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('223'))
        }])
        df = pd.concat([df, r])

        '''Obrigações fiscais a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'ObrigacoesFiscaisALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('224'))
        }])
        df = pd.concat([df, r])

        '''Provisões a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'ProvisoesALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('227'))
        }])
        df = pd.concat([df, r])

        '''Demais obrigações a longo prazo'''
        r = pd.DataFrame([{
            'Linha': 'DemaisObrigacoesALongoPrazo',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('228'))
        }])
        df = pd.concat([df, r])

        '''Resultado diferido'''
        r = pd.DataFrame([{
            'Linha': 'ResultadoDiferido',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('229'))
        }])
        df = pd.concat([df, r])

        '''Patrimônio Líquido'''
        r = pd.DataFrame([{
            'Linha': 'PatrimonioLiquido',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('23'))
        }])
        df = pd.concat([df, r])

        '''Patrimônio social e capital social'''
        r = pd.DataFrame([{
            'Linha': 'PatrimonioSocialECapitalSocial',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('231'))
        }])
        df = pd.concat([df, r])

        '''Adiantamento para futuro aumento de capital'''
        r = pd.DataFrame([{
            'Linha': 'AdiantamentoParaFuturoAumentoDeCapital',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('232'))
        }])
        df = pd.concat([df, r])

        '''Reservas de capital'''
        r = pd.DataFrame([{
            'Linha': 'ReservasDeCapital',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('233'))
        }])
        df = pd.concat([df, r])

        '''Ajustes de avaliação patrimonial'''
        r = pd.DataFrame([{
            'Linha': 'AjustesDeAvaliacaoPatrimonial',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('234'))
        }])
        df = pd.concat([df, r])

        '''Reservas de lucros'''
        r = pd.DataFrame([{
            'Linha': 'ReservasDeLucros',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('235'))
        }])
        df = pd.concat([df, r])

        '''Demais reservas'''
        r = pd.DataFrame([{
            'Linha': 'DemaisReservas',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('236'))
        }])
        df = pd.concat([df, r])

        '''Resultados acumulados'''
        r = pd.DataFrame([{
            'Linha': 'ResultadosAcumulados',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('237'))
        }])
        df = pd.concat([df, r])

        '''Ações e cotas em tesouraria'''
        r = pd.DataFrame([{
            'Linha': 'AcoesCotasEmTesouraria',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('239'))
        }])
        df = pd.concat([df, r])

        '''Total do Passivo e PL'''
        '''Ações e cotas em tesouraria'''
        r = pd.DataFrame([{
            'Linha': 'PassivoEPLTotal',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('2'))
        }])
        df = pd.concat([df, r])

        df_ant = self.load_ano_anterior(frame)
        df = self.merge_atual_anterior(df, df_ant, 'ExercicioAnterior', 'ExercicioAtual')

        self.save(df, frame)

    def merge_atual_anterior(self, atual, anterior, novo_campo, campo_anterior):
        atual[novo_campo] = 0.0
        valor = []
        for i, r in atual.iterrows():
            linha = r['Linha']
            if anterior['Linha'].isin([linha]).any():
                valor.append(anterior[anterior['Linha'] == linha][campo_anterior].sum())
        atual[novo_campo] = valor
        return atual
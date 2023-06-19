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
        df.to_excel(output, sheet_name=frame)

    def sum(self, df, col, filter):
        return round(df[filter][col].sum(), 2)

    def load_quadro_principal(self):
        bverenc = self.bverenc
        df = pd.DataFrame(columns=['Linha', 'ExercicioAtual'])

        r = pd.DataFrame([{
            'Linha': 'AtivoCirculante',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final', bverenc['conta_contabil'].astype(str).str.startswith('11'))
        }])
        df = pd.concat([df, r])

        r = pd.DataFrame([{
            'Linha': 'CaixaEEquivalentesDeCaixa',
            'ExercicioAtual': self.sum(bverenc, 'saldo_final',
                                       bverenc['conta_contabil'].astype(str).str.startswith('111'))
        }])
        df = pd.concat([df, r])

        self.save(df, 'QuadroPrincipal')

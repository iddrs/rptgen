"""Pacote para geração de relatórios contábeis, orçamentários e financeiros."""

import argparse
import configparser
from os.path import isfile

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ano', required=True, type=int)
    parser.add_argument('--mes', required=True, type=int)
    parser.add_argument('--escopo', required=True, type=int)
    return parser.parse_args()


def load_config(config_file):
    if not isfile(config_file):
        raise Exception(f'Arquivo de configuração {config_file} não encontrado!')
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

class DataRepo:
    def __init__(self, data):
        self.data = data

    def get(self, frame, linha, campo):
        df = self.data[frame]
        return df[df['Linha'] == linha][campo].sum()

    def get_frame(self, frame):
        return self.data[frame]

    def get_campo(self, frame, campo):
        return self.data[frame][campo]

    def get_linha(self, frame, linha):
        df = self.data[frame]
        return df[df['Linha'] == linha]
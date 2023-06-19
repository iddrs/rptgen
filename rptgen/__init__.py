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
"""Pacote para geração de relatórios contábeis, orçamentários e financeiros."""

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ano', required=True, type=int)
    parser.add_argument('--mes', required=True, type=int)
    parser.add_argument('--escopo', required=True, type=int)
    return parser.parse_args()

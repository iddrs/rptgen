import argparse

from typeguard import typechecked

from rptgen import log
from rptgen.escopo import Escopo

logger = log.get_logger(__name__)


@typechecked
def get_args() -> argparse.Namespace:
    """Função para obter os argumentos de linha de comando.

    Retorno
    -------
    argparse.Namespace
        Namespace contendo os argumentos de linha de comando.
    """
    argparser = argparse.ArgumentParser(prog='RtpGen',
                                        usage='Gerador de relatórios.',
                                        description='Gerador de relatórios da DCASP.',
                                        add_help=True,
                                        allow_abbrev=True,
                                        exit_on_error=True)
    argparser.add_argument('acao', action='store', type=str, help='Ação a realizar.', choices=['prepare', 'build'])
    argparser.add_argument('--ano', action='store', type=int, required=True, help='Ano base do relatório [AAAA]',
                           dest='ano')
    argparser.add_argument('--mes', action='store', type=int, required=True, help='Mês base do relatório [MM]',
                           dest='mes')
    argparser.add_argument('--escopo', action='store', type=Escopo, required=True, help='Escopo do relatório',
                           dest='escopo', choices=Escopo)
    args = argparser.parse_args()
    return args

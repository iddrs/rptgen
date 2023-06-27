import logging

from dotenv import dotenv_values
from typeguard import typechecked


@typechecked
def get_logger(name: str) -> logging:
    """Função para obter um logger com configurações baseadas no ambiente.

    Para exibir avisos no nível DEBUG, configure DEV_MODE=True no arquivo .env.

    Parâmetros
    ----------
    name : str
        Nome do logger.

    Retorno
    -------
    logging.Logger
        Instância do logger com o nome e configurações especificadas.
    """
    env = dotenv_values('.env')
    if env['DEV_MODE'] == 'True':
        level = logging.DEBUG
        fmt = '%(levelname)s    %(pathname)s:%(lineno)d    %(message)s'
    else:
        level = logging.INFO
        fmt = '%(levelname)s    %(message)s'

    logging.basicConfig(level=level, format=fmt)
    return logging.getLogger(name)

import logging

from dotenv import dotenv_values
from typeguard import typechecked


@typechecked
def get_logger(name: str) -> logging:
    env = dotenv_values('.env')
    if env['DEV_MODE'] == 'True':
        level = logging.DEBUG
        fmt = '%(levelname)s    %(pathname)s:%(lineno)d    %(message)s'
    else:
        level = logging.INFO
        fmt = '%(levelname)s    %(message)s'

    logging.basicConfig(level=level, format=fmt)
    return logging.getLogger(name)

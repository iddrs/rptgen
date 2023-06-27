import logging

from dotenv import dotenv_values
from typeguard import typechecked


@typechecked
def get_logger(name: str) -> logging:
    env = dotenv_values('.env')
    if env['DEV_MODE'] == 'True':
        level = logging.DEBUG
        format = '%(levelname)s    %(pathname)s:%(lineno)d    %(message)s'
    else:
        level = logging.INFO
        format = '%(levelname)s    %(message)s'

    logging.basicConfig(level=level, format=format)
    return logging.getLogger(name)

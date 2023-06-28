import argparse
import os

import pandas as pd
from typeguard import typechecked

import cfg
from dcasp.prepare.bp import Prepare
from dcasp.prepare.reader import PadReader
from dcasp.prepare.writer import ExcelWriterBase
from rptgen import log
from rptgen.escopo import Escopo
from rptgen.frame import Frames

logger = log.get_logger(__name__)


@typechecked
def extract(args: argparse.Namespace) -> dict:
    """Extrai os dados brutos com base nos argumentos especificados.

    Parâmetros
    ----------
    args : argparse.Namespace
        Namespace contendo os argumentos de linha de comando.

    Retorno
    -------
    dict[str, pd.DataFrame]
        Dicionário contendo os DataFrames com os dados brutos extraídos.
    """
    logger.info('Carregando os dados brutos...')
    source_dir = os.path.join(cfg.Pad.BASE_DIR, f'{str(args.ano)}-{str(args.mes).zfill(2)}', 'parquet')
    logger.debug(f'Dados de origem: {source_dir}')
    rdr = PadReader(base_dir=source_dir)
    bverenc = rdr.read('BVER_ENC.parquet')
    logger.debug(f'bverenc importado: {bverenc.shape}')
    return {
        'bverenc': bverenc
    }


@typechecked
def transform(escopo: Escopo, **kwargs: pd.DataFrame) -> Frames:
    """Transforma os dados brutos com base no escopo especificado.

    Parâmetros
    ----------
    escopo : Escopo
        Escopo dos dados a serem transformados.
    kwargs : pd.DataFrame
        Dicionário contendo os DataFrames com os dados brutos a serem transformados.

    Retorno
    -------
    Frames
        Instância da classe Frames contendo os DataFrames com os dados transformados.
    """
    logger.info('Transformando os dados...')
    transformer = Prepare(escopo=escopo, **kwargs)
    frames = transformer.prepare()
    logger.debug(f'Frames produzidos: {frames.names()}')
    return frames


@typechecked
def load(filepath: str, frames: Frames):
    """Salva os dados transformados no arquivo especificado.

    Parâmetros
    ----------
    filepath : str
        Caminho do arquivo a ser escrito.
    frames : Frames
        Instância da classe Frames contendo os DataFrames a serem escritos.
    """
    logger.info('Salvando os dados transformados...')
    logger.debug(f'Salvando em: {filepath}')
    wrtr = ExcelWriterBase(filepath)
    wrtr.write(frames)

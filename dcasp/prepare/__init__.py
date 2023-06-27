from dcasp.prepare.writer import ExcelWriter
from rptgen.escopo import Escopo
from rptgen.frame import Frames
import pandas as pd
import os
from rptgen import log
from dcasp.prepare.reader import PadReader
import cfg
import argparse
from dcasp.prepare.bp import Prepare

logger = log.get_logger(__name__)

def extract(args: argparse.Namespace) -> dict:
    logger.info('Carregando os dados brutos...')
    source_dir = os.path.join(cfg.pad.BASE_DIR, f'{str(args.ano)}-{str(args.mes).zfill(2)}', 'parquet')
    logger.debug(f'Dados de origem: {source_dir}')
    reader = PadReader(base_dir=source_dir)
    bverenc = reader.read('BVER_ENC.parquet')
    logger.debug(f'bverenc importado: {bverenc.shape}')
    return {
        'bverenc': bverenc
    }


def transform(escopo: Escopo, **kwargs: pd.DataFrame) -> Frames:
    logger.info('Transformando os dados...')
    transformer = Prepare(escopo=escopo, **kwargs)
    frames = transformer.prepare()
    logger.debug(f'Frames produzidos: {frames.names()}')
    return frames

def load(filepath: str, frames: Frames):
    logger.info('Salvando os dados transformados...')
    logger.debug(f'Salvando em: {filepath}')
    writer = ExcelWriter(filepath)
    writer.write(frames)
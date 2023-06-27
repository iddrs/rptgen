"""Balanço Patrimonial / DCASP"""

import os
from rptgen import log
from dcasp import get_args
import cfg
from dcasp.prepare import extract, transform, load

logger = log.get_logger(__name__)

args = get_args()
logger.info('Processo iniciado para DCASP...')
logger.debug(args)

if args.acao == 'prepare':
    logger.info('Preparando os dados...')
    logger.debug(args)
    data = extract(args)
    frames = transform(escopo=args.escopo, **data)
    filepath = os.path.join(cfg.rptgen.DATA_BASE_DIR, cfg.dcasp.BASE_OUTPUT_DIR, f'{str(args.ano)}',
                                   f'{str(args.mes).zfill(2)}', str(args.escopo), 'bp.xlsx')
    logger.debug(f'Arquivo de destino: {filepath}')
    load(filepath, frames)

elif args.acao == 'build':
    destination_dir = os.path.join(cfg.rptgen.OUTPUT_BASE_DIR, cfg.dcasp.BASE_OUTPUT_DIR, f'{str(args.ano)}', f'{str(args.mes).zfill(2)}', str(args.escopo))
    logger.debug(f'Destino dos dados transformados: {destination_dir}')
else:
    raise Exception(f'Ação {args.acao} inválida.')


logger.info('Processo concluído!')
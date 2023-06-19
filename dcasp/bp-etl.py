"""ETL para o Balanço Patrimonial"""
import sys
sys.path.insert(0, '../')

from rptgen.dcasp.bp import ETL, Escopo
from rptgen import parse_args, load_config

args = parse_args()
config = load_config('../config.ini')
etl = ETL(config=config, ano=args.ano, mes=args.mes, escopo=Escopo(args.escopo))
etl.run()

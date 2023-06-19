"""ETL para o Balanço Patrimonial"""
import sys
sys.path.insert(0, '../')

from rptgen.dcasp.bp import ETL, Escopo
from rptgen import parse_args

args = parse_args()

etl = ETL(ano=args.ano, mes=args.mes, escopo=Escopo(args.escopo))
etl.run()

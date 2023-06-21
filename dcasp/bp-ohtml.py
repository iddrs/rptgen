"""Output para HTML do Balanço Patrimonial"""
import sys
sys.path.insert(0, '../')

from rptgen.dcasp.bp import Escopo
from rptgen.dcasp.bp.output.html import HTMLOutput as Output
from rptgen import parse_args, load_config

args = parse_args()
config = load_config('../config.ini')
output = Output(config=config, ano=args.ano, mes=args.mes, escopo=Escopo(args.escopo))
output.run()

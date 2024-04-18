select sum(saldo_inicial)::decimal from pad.bver_enc%s
where remessa = %d
and entidade in %s
and escrituracao like 'S'
and conta_contabil like '1%%'
and indicador_superavit_financeiro like 'F'
select sum(saldo_inicial)::decimal from pad.bal_ver%s
where remessa = %d
and entidade in %s
and escrituracao like 'S'
and conta_contabil like '%s'
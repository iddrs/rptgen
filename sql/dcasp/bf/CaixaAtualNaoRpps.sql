select sum(saldo_atual)::decimal from pad.bver_enc%s
where remessa = %d
and entidade in %s
and escrituracao like 'S'
and conta_contabil like '%s'
and entidade not like 'fpsm'
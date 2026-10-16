select
    date_trunc('month', v.dt_aplicacao) as mes,
    v.co_imunobiologico,
    count(*) as doses_aplicadas,
    count(distinct vc.prontuario_id) as cidadaos_vacinados
from {{ ref('stg_vacinacao') }} v
join {{ ref('stg_vacinacao_cidadao') }} vc on vc.vacinacao_link_id = v.co_vacinacao
group by 1, 2
order by 1, 2

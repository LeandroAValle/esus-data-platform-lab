select
    eq.equipe_id,
    eq.no_equipe,
    us.unidade_saude_id,
    us.no_unidade_saude,
    date_trunc('month', a.dt_inicio) as mes,
    count(*) as total_visitas
from {{ ref('stg_atendimento') }} a
join {{ ref('stg_equipe') }} eq on eq.equipe_id = a.equipe_id
join {{ ref('stg_unidade_saude') }} us on us.unidade_saude_id = a.unidade_saude_id
where a.is_visita_domiciliar
group by 1, 2, 3, 4, 5
order by 5, 1

select
    eq.equipe_id,
    eq.no_equipe,
    date_trunc('month', a.dt_inicio) as mes,
    count(*) as total_atendimentos,
    count(*) filter (where a.is_visita_domiciliar) as total_visitas_domiciliares
from {{ ref('stg_atendimento') }} a
join {{ ref('stg_equipe') }} eq using (equipe_id)
group by 1, 2, 3
order by 3, 1

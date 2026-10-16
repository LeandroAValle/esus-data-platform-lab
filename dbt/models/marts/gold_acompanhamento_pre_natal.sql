select
    count(*) as total_gestacoes,
    count(*) filter (where dt_desfecho is null) as gestacoes_em_andamento,
    count(*) filter (where st_alto_risco = 1) as gestacoes_alto_risco,
    count(*) filter (where st_gravidez_planejada = 1) as gestacoes_planejadas
from {{ ref('stg_pre_natal') }}

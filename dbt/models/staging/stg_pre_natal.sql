select
    pn.co_seq_pre_natal as pre_natal_id,
    pr.cidadao_id,
    pn.dt_ultima_menstruacao,
    pn.dt_desfecho,
    pn.st_gravidez_planejada,
    pn.st_alto_risco
from {{ source('silver', 'pre_natal') }} pn
left join {{ ref('stg_prontuario') }} pr on pr.prontuario_id = pn.co_prontuario

select
    co_seq_registro_vacinacao as vacinacao_id,
    co_vacinacao,
    co_imunobiologico,
    co_dose_imunobiologico,
    co_estrategia_vacinacao,
    dt_aplicacao
from {{ source('silver', 'vacinacao') }}
where dt_aplicacao is not null

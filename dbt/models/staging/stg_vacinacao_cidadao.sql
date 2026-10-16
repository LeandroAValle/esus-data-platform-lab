-- liga registro de vacinação (silver.vacinacao) ao cidadão, via
-- tb_vacinacao -> prontuário -> cidadão
select
    v.co_seq_vacinacao as vacinacao_link_id,
    v.co_prontuario as prontuario_id
from {{ source('bronze', 'tb_vacinacao') }} v
where v.co_prontuario is not null

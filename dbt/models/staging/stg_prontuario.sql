select
    co_seq_prontuario as prontuario_id,
    co_cidadao as cidadao_id
from {{ source('bronze', 'tb_prontuario') }}
where co_cidadao is not null

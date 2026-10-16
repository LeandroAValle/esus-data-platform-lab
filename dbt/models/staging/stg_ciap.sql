select
    co_seq_ciap as ciap_id,
    co_ciap as ciap_codigo,
    ds_ciap as ciap_descricao
from {{ source('bronze', 'tb_ciap') }}

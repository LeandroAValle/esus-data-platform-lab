select
    co_cid10 as cid10_id,
    nu_cid10 as cid10_codigo,
    no_cid10 as cid10_descricao
from {{ source('bronze', 'tb_cid10') }}

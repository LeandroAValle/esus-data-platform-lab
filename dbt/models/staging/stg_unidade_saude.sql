select
    co_seq_unidade_saude as unidade_saude_id,
    no_unidade_saude,
    nu_cnes,
    st_ativo
from {{ source('silver', 'unidade_saude') }}
where co_seq_unidade_saude is not null

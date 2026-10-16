select
    co_seq_equipe as equipe_id,
    co_unidade_saude as unidade_saude_id,
    no_equipe,
    nu_ine,
    tp_equipe,
    st_ativo
from {{ source('silver', 'equipe') }}
where co_seq_equipe is not null

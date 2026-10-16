select
    co_unico_lotacao as lotacao_id,
    co_prof as profissional_id,
    co_unidade_saude as unidade_saude_id,
    co_equipe as equipe_id,
    co_cbo,
    dt_desativacao_lotacao is null as ativo
from {{ source('silver', 'lotacao') }}
where co_prof is not null

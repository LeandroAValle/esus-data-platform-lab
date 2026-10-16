select
    co_seq_atend as atendimento_id,
    co_prontuario as prontuario_id,
    co_unidade_saude as unidade_saude_id,
    co_equipe as equipe_id,
    dt_inicio,
    tp_local_atend,
    tp_local_atend = 4 as is_visita_domiciliar,
    st_atend
from {{ source('silver', 'atendimento') }}
where dt_inicio is not null

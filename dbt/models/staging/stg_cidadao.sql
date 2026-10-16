select
    co_seq_cidadao as cidadao_id,
    nu_cpf,
    nu_cns,
    dt_nascimento,
    date_diff('year', dt_nascimento, current_date) as idade,
    no_sexo,
    st_ativo,
    st_faleceu
from {{ source('silver', 'cidadao') }}
where co_seq_cidadao is not null

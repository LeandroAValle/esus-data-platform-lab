select
    c.cidadao_id,
    c.idade,
    c.no_sexo
from {{ ref('stg_cidadao') }} c
join {{ ref('stg_condicoes_cronicas') }} cc using (cidadao_id)
where cc.hipertenso and c.st_ativo = 1

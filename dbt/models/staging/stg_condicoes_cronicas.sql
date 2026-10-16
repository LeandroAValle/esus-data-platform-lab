-- condição crônica por cidadão: autorreferida (ficha de cadastro) OU
-- diagnosticada (CIAP K86/K87 hipertensão, T89/T90 diabetes; CID10 I10,
-- E10-E14) — o que vier primeiro já classifica o cidadão.
with autorreferida as (
    select
        co_cidadao as cidadao_id,
        coalesce(st_hipertensao_arterial, 0) = 1 as hipertenso_autorreferido,
        coalesce(st_diabetes, 0) = 1 as diabetico_autorreferido
    from {{ source('silver', 'condicoes_saude_auto') }}
    where co_cidadao is not null
),
diagnosticada as (
    select
        cidadao_id,
        bool_or(ciap_codigo in ('K86', 'K87') or cid10_codigo like 'I10%') as hipertenso_diagnosticado,
        bool_or(ciap_codigo in ('T89', 'T90') or cid10_codigo similar to 'E1[0-4]%') as diabetico_diagnosticado
    from {{ ref('stg_problema') }}
    group by cidadao_id
)
select
    coalesce(a.cidadao_id, d.cidadao_id) as cidadao_id,
    coalesce(a.hipertenso_autorreferido, false) or coalesce(d.hipertenso_diagnosticado, false) as hipertenso,
    coalesce(a.diabetico_autorreferido, false) or coalesce(d.diabetico_diagnosticado, false) as diabetico
from autorreferida a
full outer join diagnosticada d on d.cidadao_id = a.cidadao_id

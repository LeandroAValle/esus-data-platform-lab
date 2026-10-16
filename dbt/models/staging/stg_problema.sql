-- diagnóstico formal (CIAP/CID) por cidadão, via prontuário
select
    p.co_seq_problema as problema_id,
    pr.cidadao_id,
    cid.cid10_codigo,
    ciap.ciap_codigo
from {{ source('silver', 'problema') }} p
left join {{ ref('stg_prontuario') }} pr on pr.prontuario_id = p.co_prontuario
left join {{ ref('stg_cid10') }} cid on cid.cid10_id = p.co_cid10
left join {{ ref('stg_ciap') }} ciap on ciap.ciap_id = p.co_ciap
where pr.cidadao_id is not null

"""
Classificação de colunas por tabela da base e-SUS para redução de PII na
camada Bronze.

- hash: identificador direto (CPF, CNS, nome) — mantido como hash SHA-256
  com salt, preservando a capacidade de join sem expor o dado real.
- drop: contato/endereço/texto livre sem valor analítico para os
  indicadores do projeto — removido por completo.
- (não listado): mantido como está (dado clínico/demográfico/código de
  domínio, necessário para os indicadores).
"""

TABLES: dict[str, dict[str, list[str]]] = {
    "ta_cidadao": {
        "hash": [
            "nu_cpf",
            "nu_cns",
            "co_unico_cidadao",
            "co_unico_cidadao_prontuario",
            "co_unico_prontuario",
            "co_unico_ultima_ficha",
            "nu_cns_responsavel",
            "nu_cns_cuidador",
            "nu_cpf_cuidador",
            "nu_cpf_responsavel",
        ],
        "drop": [
            "no_cidadao",
            "no_cidadao_filtro",
            "no_mae",
            "no_mae_filtro",
            "no_pai",
            "no_social",
            "no_responsavel",
            "no_cuidador",
            "ds_logradouro",
            "ds_complemento",
            "ds_ponto_referencia",
            "no_bairro",
            "no_bairro_filtro",
            "ds_cep",
            "nu_numero",
            "nu_telefone_residencial",
            "nu_telefone_celular",
            "nu_telefone_contato",
            "ds_email",
            "no_localidade_exterior",
            "nu_documento_obito",
            "nu_dnv",
            "nu_nis_pis_pasep",
        ],
    },
    "ta_atend": {
        "hash": ["co_unico_atend"],
        "drop": ["no_justificativa_reg_tardio"],
    },
    "ta_atend_prof": {
        "hash": ["co_unico_atend_prof"],
        "drop": ["nu_conselho_classe"],
    },
    "ta_registro_vacinacao": {
        "hash": ["co_unico_registro_vacinacao"],
        "drop": ["ds_observacoes"],
    },
    "ta_atend_prof_pre_natal": {
        "hash": [],
        "drop": [],
    },
    "ta_cidadao_vinculacao_equipe": {
        "hash": [],
        "drop": [],
    },
    "ta_unidade_saude": {
        "hash": [],
        "drop": [
            "nu_cnpj",
            "nu_licenca_funcionamento",
            "nu_telefone_comercial",
            "nu_telefone_comercial2",
            "nu_telefone_fax",
            "ds_email",
            "ds_cep",
            "ds_complemento",
            "ds_ponto_referencia",
            "ds_logradouro",
            "nu_numero",
            "no_bairro",
            "no_bairro_filtro",
        ],
    },
    "ta_equipe": {
        "hash": [],
        "drop": [],
    },
    "ta_prof": {
        "hash": ["nu_cpf", "nu_cns"],
        "drop": [
            "no_profissional",
            "no_profissional_filtro",
            "no_social_profissional",
            "no_civil_profissional",
            "nu_telefone",
            "ds_email",
            "ds_cep",
            "ds_complemento",
            "ds_ponto_referencia",
            "ds_logradouro",
            "nu_numero",
            "no_bairro",
            "no_bairro_filtro",
            "nu_conselho_classe",
        ],
    },
    "ta_lotacao": {"hash": ["co_unico_lotacao"], "drop": []},
    "ta_pre_natal": {"hash": [], "drop": []},
    "ta_exame_prenatal": {"hash": [], "drop": []},
    "ta_condicoes_saude_cardiaca": {"hash": [], "drop": []},
    "ta_problema": {"hash": ["co_unico_problema", "nu_uuid_problema"], "drop": []},
    "ta_cidadao_grupo": {
        "hash": ["nu_cns", "nu_cpf", "nu_uuid_ultima_ficha", "nu_uuid_origem"],
        "drop": [],
    },
    "ta_cds_domicilio": {
        "hash": ["nu_cns", "nu_cns_responsavel_tecnico", "co_unico_domicilio", "co_unico_ultima_ficha"],
        "drop": [
            "no_logradouro",
            "no_logradouro_filtro",
            "ds_complemento",
            "no_bairro",
            "no_bairro_filtro",
            "ds_cep",
            "nu_fone_referencia",
            "nu_fone_residencia",
            "ds_ponto_referencia",
            "no_instituicao_permanencia",
            "no_responsavel_tecnico",
            "nu_contato_responsavel_tecnico",
            "nu_latitude",
            "nu_longitude",
        ],
    },
    "ta_exame_hemoglobina_glicada": {"hash": [], "drop": []},
    "ta_medicamento_uso_continuo": {"hash": [], "drop": []},
    "ta_medicamento": {"hash": [], "drop": []},
    "ta_vacinacao": {"hash": [], "drop": []},
    "ta_imunobiologico_lote": {"hash": [], "drop": []},
}

# Padrões heurísticos usados apenas para as tabelas de domínio/lookup
# (tb_*, rl_*), descobertas dinamicamente em runtime — não são revisadas
# manualmente porque são ~700+ tabelas majoritariamente de código/descrição,
# então esta é uma rede de segurança, não a regra principal de privacidade.
#
# IMPORTANTE: um levantamento em todas as colunas `no_*` de tb_*/rl_* (540
# colunas) mostrou que a maioria é rótulo de catálogo (no_tipo_atend,
# no_grupo_exame, etc. — seguros), mas várias são nome de pessoa de fato
# (no_cidadao, no_mae, no_profissional...) e não seguem um padrão previsível
# o suficiente pra confiar só em substring simples. Por isso, além dos
# padrões diretos abaixo, qualquer coluna com prefixo "no_" (nome) que
# contenha uma das PII_NAME_KEYWORDS é dropada por padrão — postura
# fail-safe (superdropar é aceitável; vazar nome real não é).
PII_NAME_PATTERNS_HASH = ("nu_cpf", "nu_cns", "co_unico_")
PII_NAME_PATTERNS_DROP = (
    "no_nome",
    "no_mae",
    "no_pai",
    "no_responsavel",
    "no_cuidador",
    "ds_email",
    "no_email",
    "ds_logradouro",
    "no_logradouro",
    "no_bairro",
    "nu_telefone",
    "nu_fone",
    "ds_cep",
    "nu_latitude",
    "nu_longitude",
    "no_usuario",
)

# Aplicado apenas a colunas cujo nome começa com "no_" (ver nota acima).
PII_NAME_KEYWORDS_ON_NO_PREFIX = (
    "cidadao",
    "mae",
    "pai",
    "respons",
    "cuidador",
    "social",
    "email",
    "usuario",
    "executante",
    "finalizador",
    "solicitante",
    "profissional",
    "chefe",
    "servidor",
    "autor",
)

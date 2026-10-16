# Dicionário de Dados — Bronze (fonte: e-SUS)

Gerado a partir dos metadados nativos (`COMMENT ON`) do schema de origem.
Colunas marcadas com `[hash]` ou `[drop]` foram pseudonimizadas/removidas na Bronze — ver [src/ingestion/pii_config.py](../src/ingestion/pii_config.py). Isso não garante anonimização do conjunto.

Cobre apenas as 21 tabelas operacionais curadas (revisão manual de PII). As
~731 tabelas de domínio/lookup (`tb_*`, `rl_*`) são descobertas em runtime e
classificadas por heurística de nome de coluna — ver
[src/ingestion/domain_tables.py](../src/ingestion/domain_tables.py).

**Limitação conhecida:** algumas tabelas falham por data-sentinela inválida
na fonte (dado legado do e-SUS, ex. `year -1 is out of range`). Não bloqueiam
os indicadores do escopo. Na extração (raw): `tb_cds_domicilio_familia`,
`tb_familia`. Na conversão pra Delta (Bronze): `tb_cds_atend_individual`,
`tb_cds_ativ_col_participante`, `tb_cds_cad_individual`, `tb_cds_proced`,
`tb_cds_visita_domiciliar` — todas do módulo CDS (ficha de coleta de dados
simplificada), mesma causa raiz. Retomar tratando as colunas de data
problemáticas como texto na query/leitura, se algum dia forem necessárias.

## ta_cidadao
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_tacidadao | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_seq_cidadao | bigint |  | mantida |
| co_unico_cidadao_prontuario | character varying(36) |  | hash |
| co_unico_prontuario | character varying(36) |  | hash |
| st_desconhece_nome_mae | integer |  | mantida |
| co_localidade | bigint |  | mantida |
| nu_area | character varying(3) |  | mantida |
| nu_micro_area | character varying(3) |  | mantida |
| nu_nis_pis_pasep | character varying(50) |  | drop |
| dt_atualizado | timestamp(6) without time zone |  | mantida |
| nu_cns_responsavel | character varying(16) |  | hash |
| no_responsavel | character varying(255) |  | drop |
| dt_nascimento_responsavel | timestamp(6) without time zone |  | mantida |
| nu_cns_cuidador | character varying(16) |  | hash |
| no_cuidador | character varying(255) |  | drop |
| dt_nascimento_cuidador | timestamp(6) without time zone |  | mantida |
| tp_cds_cuidador | bigint |  | mantida |
| co_unico_cidadao | character varying(96) |  | hash |
| co_nacionalidade | bigint |  | mantida |
| co_pais_nascimento | bigint |  | mantida |
| co_unico_ultima_ficha | character varying(96) |  | hash |
| dt_ultima_ficha | date |  | mantida |
| st_registro_cadsus | integer |  | mantida |
| dt_atualizado_cadsus | date |  | mantida |
| st_desconhece_nome_pai | integer |  | mantida |
| dt_naturalizacao | timestamp with time zone |  | mantida |
| dt_entrada_brasil | timestamp with time zone |  | mantida |
| nu_portaria_naturalizacao | character varying(16) |  | mantida |
| st_fora_area | integer |  | mantida |
| st_infrm_orientacao_sexual | integer |  | mantida |
| tp_orientacao_sexual | character varying(25) |  | mantida |
| st_infrm_identidade_genero | integer |  | mantida |
| tp_identidade_genero | character varying(25) |  | mantida |
| st_compartilhamento_prontuario | integer |  | mantida |
| st_ativo | integer |  | mantida |
| st_nao_possui_cuidador | integer |  | mantida |
| nu_cpf | character varying(11) |  | hash |
| nu_cns | character varying(16) |  | hash |
| no_cidadao | character varying(500) |  | drop |
| no_cidadao_filtro | character varying(600) |  | drop |
| co_escolaridade | bigint |  | mantida |
| co_raca_cor | bigint |  | mantida |
| co_etnia | bigint |  | mantida |
| co_estado_civil | bigint |  | mantida |
| co_cbo | bigint |  | mantida |
| dt_nascimento | date |  | mantida |
| dt_obito | date |  | mantida |
| no_mae | character varying(500) |  | drop |
| no_mae_filtro | character varying(600) |  | drop |
| no_pai | character varying(500) |  | drop |
| no_social | character varying(255) |  | drop |
| st_faleceu | integer |  | mantida |
| nu_documento_obito | character varying(255) |  | drop |
| st_dados_obito_cadsus | integer |  | mantida |
| no_localidade_exterior | character varying(255) |  | drop |
| co_pais_exterior | bigint |  | mantida |
| ds_cep | character varying(8) |  | drop |
| ds_complemento | character varying(50) |  | drop |
| ds_ponto_referencia | character varying(100) |  | drop |
| ds_logradouro | character varying(150) |  | drop |
| co_uf | bigint |  | mantida |
| co_localidade_endereco | bigint |  | mantida |
| nu_numero | character varying(20) |  | drop |
| st_sem_numero | integer |  | mantida |
| no_bairro | character varying(255) |  | drop |
| no_bairro_filtro | character varying(255) |  | drop |
| tp_logradouro | bigint |  | mantida |
| nu_telefone_residencial | character varying(255) |  | drop |
| nu_telefone_celular | character varying(255) |  | drop |
| nu_telefone_contato | character varying(255) |  | drop |
| ds_email | character varying(255) |  | drop |
| st_ativo_para_exibicao | integer |  | mantida |
| st_unificado | integer |  | mantida |
| st_territorio_utiliza_cpf | integer |  | mantida |
| nu_cpf_cuidador | character varying(11) |  | hash |
| nu_cpf_responsavel | character varying(11) |  | hash |
| no_tipo_sanguineo | character varying(22) |  | mantida |
| no_sexo | character varying(24) |  | mantida |
| co_aldeia_residencia | bigint | Código da aldeia referente a aldeia de residência. Chave estrangeira com origem na tabela TB_ALDEIA. | mantida |
| co_tipo_endereco | bigint | Refere-se a informação do tipo de endereco da residência. Chave estrangeira com origem na tabela TB_TIPO_ENDERECO | mantida |
| co_polo_base_residencia | bigint | Chave estrangeira com origem na tabela TB_POLO_BASE. Refere-se a informação do Polo Base de residência. | mantida |
| co_dsei_residencia | bigint | Chave estrangeira com origem na tabela TB_DSEI. Refere-se a informação da DSEI de residência. | mantida |
| nu_familia | character varying(7) | Refere-se a informação do número da família. | mantida |
| st_cpf_recebido_cadsus | integer | Indica se o CPF foi recebido do CADSUS. | mantida |
| nu_dnv | character varying(15) | Número da Declaração de Nascido Vivo. | drop |
| st_nao_possui_cpf | integer | Indica se o cidadão não possui CPF. | mantida |
| co_justifica_nao_possui_cpf | bigint | Chave estrangeira para a tabela de domínio de justificativas para não possuir CPF. | mantida |
| dt_ultima_recusa | date | Data da ultima recusa de cadastro do cidadao. | mantida |

## ta_atend
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_taatend | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_seq_atend | bigint |  | mantida |
| dt_fim | timestamp(6) without time zone |  | mantida |
| dt_inicio | timestamp(6) without time zone |  | mantida |
| qt_referencia | bigint |  | mantida |
| st_atend | bigint |  | mantida |
| co_agendado | bigint |  | mantida |
| co_responsavel | bigint |  | mantida |
| co_classificacao_risco | bigint |  | mantida |
| co_prontuario | bigint |  | mantida |
| co_unidade_saude | bigint |  | mantida |
| co_atend_prof | bigint |  | mantida |
| dt_encaminhamento | timestamp(6) without time zone |  | mantida |
| st_fechado_automaticamente | integer |  | mantida |
| nu_responsavel_anterior | bigint |  | mantida |
| co_unico_atend | character varying(96) |  | hash |
| tp_local_atend | bigint |  | mantida |
| st_registro_tardio | integer |  | mantida |
| no_justificativa_reg_tardio | character varying(50) |  | drop |
| dt_criacao_registro | timestamp with time zone |  | mantida |
| dt_ultima_alteracao_status | timestamp without time zone |  | mantida |
| co_equipe | bigint |  | mantida |
| st_atend_revisao | bigint | Situação da revisão do atendimento quando ele exige revisão. Chave estrangeira com origem na tabela TB_STATUS_REVISAO_ATEND. | mantida |

## ta_atend_prof
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_taatendprof | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_seq_atend_prof | bigint |  | mantida |
| dt_fim | timestamp(6) without time zone |  | mantida |
| dt_inicio | timestamp(6) without time zone |  | mantida |
| co_atend | bigint |  | mantida |
| co_atend_prof_tipo_encam_intrn | bigint |  | mantida |
| co_lotacao | bigint |  | mantida |
| tp_atend_prof | bigint |  | mantida |
| st_atend_prof | bigint |  | mantida |
| st_atend_enviado | integer |  | mantida |
| co_unico_ad_cidadao | bigint |  | mantida |
| co_classificacao_risco | bigint |  | mantida |
| co_unico_atend_prof | character varying(96) |  | hash |
| tp_atend | bigint |  | mantida |
| nu_conselho_classe | character varying(100) |  | drop |
| co_uf_emissora_conselho_classe | bigint |  | mantida |
| co_conselho_classe | bigint |  | mantida |
| ds_versao_ficha | character varying(30) |  | mantida |
| co_racionalidade_saude | bigint |  | mantida |
| co_lotacao_atend_compartilhado | bigint |  | mantida |
| st_registro_historico | integer |  | mantida |
| nu_revisao | integer |  | mantida |
| st_cancelado | integer |  | mantida |
| co_estagio | bigint | Código identificador do estagiário responsável pelo atendimento. Chave estrangeira com origem na tabela TB_ESTAGIO. | mantida |
| co_marcador_consumo_alim | bigint | Código do Marcador de Consumo Alimentar. Chave estrangeira com origem em TB_MARCADOR_CONSUMO_ALIMENTAR(CO_SEQ_MARCADOR_CONSUMO_ALIM). | mantida |
| tp_participacao_cidadao | bigint | Código identificador do tipo de participação do cidadão no atendimento. Chave estrangeira com origem na tabela TB_TIPO_PARTICIPACAO_ATEND. | mantida |
| tp_participacao_prof_convidado | bigint | Código identificador do tipo de participação do profissional convidado no atendimento. Chave estrangeira com origem na tabela TB_TIPO_PARTICIPACAO_ATEND. | mantida |
| co_assinatura_eletronica_atend | bigint | Código da assinatura eletronica atend. Chave estrangeira com origem em TB_ASSINATURA_ELETRONICA_ATEND(CO_SEQ_ASSINATURA_ELETRO_ATEND). | mantida |

## ta_registro_vacinacao
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_taregistrovacinacao | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_seq_registro_vacinacao | bigint |  | mantida |
| co_estrategia_vacinacao | bigint |  | mantida |
| co_imunobiologico | bigint |  | mantida |
| co_dose_imunobiologico | bigint |  | mantida |
| co_via_adm_vacina | bigint |  | mantida |
| co_local_apl_vacina | bigint |  | mantida |
| co_vacinacao | bigint |  | mantida |
| co_tipo_registro_vacinacao | bigint |  | mantida |
| st_registro_anterior | integer |  | mantida |
| dt_aprazamento | date |  | mantida |
| dt_aplicacao | timestamp with time zone |  | mantida |
| co_imunobiologico_lote | bigint |  | mantida |
| ds_observacoes | character varying(300) |  | drop |
| co_grupo_atendimento | bigint |  | mantida |
| st_aplicado_exterior | integer |  | mantida |
| co_unico_registro_vacinacao | character varying(96) | Código único que identifica o registro de vacinação. | hash |
| co_cbo_prescritor | bigint | Especialidade do profissional que prescreveu a aplicação da vacina. Chave estrangeira com origem em TB_CBO(CO_CBO). | mantida |
| co_cid10_motivo_indicacao | bigint | Motivo da indicação à aplicação da vacina. Chave estrangeira com origem em TB_CID10(CO_CID10). | mantida |
| st_pesquisa_clinica | integer | Indicação se a vacina faz parte de uma pesquisa clínica. | mantida |
| nu_anvisa_protocolo_estudo | character varying(10) | Identifica o número do protocolo do estudo clínico autorizado pela Agência Nacional de Vigilância Sanitária para administração de vacinas. | mantida |
| nu_anvisa_protocolo_versao | character varying(10) | Identifica o número da versão do protocolo do estudo clínico autorizado pela Agência Nacional de Vigilância Sanitária para administração de vacinas. | mantida |
| nu_anvisa_numero_registro | character varying(10) | Identifica o número do registro sanitário da vacina registrado na Agência Nacional de Vigilância Sanitária. | mantida |

## ta_atend_prof_pre_natal
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_taatendprofprenatal | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_atend_prof_pre_natal | bigint |  | mantida |
| co_unico_pre_natal | bigint |  | mantida |
| tp_edema | bigint |  | mantida |
| st_gravidez_planejada | integer |  | mantida |
| st_movimentacao_fetal | integer |  | mantida |

## ta_cidadao_vinculacao_equipe
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_tacidadaovinculacaoequp | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_seq_cidadao_vinculacao_eqp | bigint |  | mantida |
| co_cidadao | bigint |  | mantida |
| co_unico_ficha | character varying(96) |  | mantida |
| co_unico_cadastro_individual | character varying(96) |  | mantida |
| st_envio | integer |  | mantida |
| ds_versao_ficha | character varying(30) |  | mantida |
| st_usar_cadastro_individual | integer |  | mantida |
| st_saida_cadastro_obito | integer |  | mantida |
| st_saida_cadastro_territorio | integer |  | mantida |
| dt_atualizacao_cadastro | timestamp with time zone |  | mantida |
| co_prof_cadastrante_cds | bigint |  | mantida |
| co_atorpapel_cadastrante_pec | bigint |  | mantida |
| tp_cds_origem | bigint |  | mantida |
| nu_cnes | character varying(7) |  | mantida |
| nu_ine | character varying(10) |  | mantida |

## ta_unidade_saude
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_taunidadesaude | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| nu_licenca_funcionamento | character varying(20) |  | drop |
| tp_unidade_saude | bigint |  | mantida |
| co_seq_unidade_saude | bigint |  | mantida |
| nu_cnes | character varying(20) |  | mantida |
| st_ativo | integer |  | mantida |
| nu_cnpj | character varying(14) |  | drop |
| no_unidade_saude | character varying(255) |  | mantida |
| no_unidade_saude_filtro | character varying(255) |  | mantida |
| nu_telefone_comercial | character varying(255) |  | drop |
| nu_telefone_comercial2 | character varying(255) |  | drop |
| nu_telefone_fax | character varying(255) |  | drop |
| ds_email | character varying(255) |  | drop |
| ds_cep | character varying(8) |  | drop |
| ds_complemento | character varying(50) |  | drop |
| ds_ponto_referencia | character varying(100) |  | drop |
| ds_logradouro | character varying(150) |  | drop |
| co_uf | bigint |  | mantida |
| co_localidade_endereco | bigint |  | mantida |
| nu_numero | character varying(20) |  | drop |
| st_sem_numero | integer |  | mantida |
| no_bairro | character varying(255) |  | drop |
| no_bairro_filtro | character varying(255) |  | drop |
| tp_logradouro | bigint |  | mantida |
| co_subtp_unidade_saude | bigint |  | mantida |
| st_cnes_reset | integer | Controla se perfis de lotações e tipos de serviço da unidade foram resetados para o padrão na importação do CNES (0 - Não; 1 - Sim). | mantida |

## ta_equipe
| Coluna | Tipo | Descrição | Bronze |
|---|---|---|---|
| co_seq_taequipe | bigint |  | mantida |
| co_tipo_auditoria | character(1) |  | mantida |
| dt_auditoria | timestamp without time zone |  | mantida |
| co_seq_equipe | bigint |  | mantida |
| nu_ine | character varying(255) |  | mantida |
| st_ativo | integer |  | mantida |
| co_unidade_saude | bigint |  | mantida |
| qt_referencia | bigint |  | mantida |
| tp_equipe | bigint |  | mantida |
| ds_area | character varying(255) |  | mantida |
| no_equipe | character varying(255) |  | mantida |
| no_equipe_filtro | character varying(255) |  | mantida |
| co_unico_equipe | character varying(255) |  | mantida |

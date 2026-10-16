# Camada Gold — Indicadores

Projeto dbt em [`dbt/`](../dbt/), rodando contra DuckDB local que lê as tabelas
Delta Lake da Silver/Bronze diretamente (`delta_scan`), sem precisar
materializar cópia intermediária. Rodar: `make gold` (ou
`dbt run --project-dir dbt --profiles-dir dbt`).

## Indicadores implementados

| Modelo | Indicador do escopo | Fonte |
|---|---|---|
| `gold_hipertensos` | Hipertensos | condição autorreferida (`tb_condicoes_saude_auto`) OU diagnóstico CIAP K86/K87 / CID10 I10 (`tb_problema`) |
| `gold_diabeticos` | Diabéticos | condição autorreferida OU diagnóstico CIAP T89/T90 / CID10 E10-E14 |
| `gold_cobertura_vacinal` | Vacinação | `tb_registro_vacinacao` + `tb_vacinacao`, por mês/imunobiológico |
| `gold_acompanhamento_pre_natal` | Acompanhamento de pré-natal | `tb_pre_natal` — total de gestações, em andamento, alto risco, planejadas |
| `gold_producao_por_ubs` | Produção por UBS | `tb_atend` agregado por unidade de saúde/mês |
| `gold_producao_por_equipe` | Produção por equipe | `tb_atend` agregado por equipe/mês |
| `gold_visitas_domiciliares` | Visitas domiciliares | `tb_atend` filtrado por `co_local_atend = 4` (Domicílio) |

## Gap conhecido: Metas da APS

O e-SUS APS não armazena metas/alvos de indicadores — isso é definido fora do
sistema (planilhas, planejamento da gestão municipal). Não há tabela fonte
pra esse indicador, então não foi modelado (não inventamos números). Se
surgir uma fonte de metas (planilha, outro sistema), dá pra montar
`gold_metas_aps` cruzando meta planejada vs. realizado dos indicadores acima.

## Limitações de qualidade de dado conhecidas

- Datas legadas corrompidas (ver [dicionario_dados.md](dicionario_dados.md)) já
  são tratadas na Silver (`sanitize_date_range`, vira NULL fora de 1900-2100),
  mas alguns registros antigos (anos 1960-70) ainda aparecem em
  `gold_producao_por_ubs`/`gold_cobertura_vacinal` — prováveis erros de
  digitação na fonte (não sentinela clássico), não seria correto tratar como
  inválido automaticamente sem revisão de negócio.
- `tb_visita_domiciliar_acs` (extraída na Bronze) não tem data e não é usada
  como fonte de visitas — usamos `tb_atend` com `co_local_atend = 4`, mais
  confiável para agregações temporais.

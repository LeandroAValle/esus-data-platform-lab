"""
Dashboard Streamlit dos indicadores da APS (camada Gold).

Lê data/lakehouse/gold.duckdb somente leitura — nunca escreve, então
pode rodar em paralelo com o dbt sem conflito de lock.

Uso: streamlit run src/dashboard/app.py
"""

import os

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="eSUS Data Platform — Indicadores APS", layout="wide")

GOLD_DB_PATH = os.environ.get("GOLD_DB_PATH", "data/lakehouse/gold.duckdb")


@st.cache_resource
def get_connection():
    return duckdb.connect(GOLD_DB_PATH, read_only=True)


@st.cache_data(ttl=300)
def query(sql: str) -> pd.DataFrame:
    return get_connection().sql(sql).df()


st.title("eSUS Data Platform — Indicadores APS")
st.caption(
    "Laboratório: use somente dados sintéticos ou autorizados; identificadores podem ser pseudonimizados. "
    "Pipeline: Postgres → Bronze (Delta) → Silver (PySpark) → Gold (dbt), orquestrado via Airflow."
)

# ---------------------------------------------------------------- filtros
producao_ubs = query("SELECT * FROM main_gold.gold_producao_por_ubs")
producao_equipe = query("SELECT * FROM main_gold.gold_producao_por_equipe")
visitas = query("SELECT * FROM main_gold.gold_visitas_domiciliares")
vacinal = query("SELECT * FROM main_gold.gold_cobertura_vacinal")
pre_natal = query("SELECT * FROM main_gold.gold_acompanhamento_pre_natal")
hipertensos = query("SELECT * FROM main_gold.gold_hipertensos")
diabeticos = query("SELECT * FROM main_gold.gold_diabeticos")

with st.sidebar:
    st.header("Filtros")
    ubs_opcoes = sorted(producao_ubs["no_unidade_saude"].dropna().unique())
    equipe_opcoes = sorted(producao_equipe["no_equipe"].dropna().unique())
    ubs_selecionadas = st.multiselect("UBS", ubs_opcoes, default=ubs_opcoes)
    equipes_selecionadas = st.multiselect("Equipe", equipe_opcoes, default=equipe_opcoes)

producao_ubs_f = producao_ubs[producao_ubs["no_unidade_saude"].isin(ubs_selecionadas)]
producao_equipe_f = producao_equipe[producao_equipe["no_equipe"].isin(equipes_selecionadas)]
visitas_f = visitas[
    visitas["no_unidade_saude"].isin(ubs_selecionadas) & visitas["no_equipe"].isin(equipes_selecionadas)
]

# ---------------------------------------------------------------- KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Hipertensos", f"{len(hipertensos):,}".replace(",", "."))
col2.metric("Diabéticos", f"{len(diabeticos):,}".replace(",", "."))
col3.metric("Gestações acompanhadas", int(pre_natal["total_gestacoes"].iloc[0]))
col4.metric("Gestações em andamento", int(pre_natal["gestacoes_em_andamento"].iloc[0]))

st.divider()

tab_producao, tab_vacinal, tab_pre_natal, tab_visitas, tab_cronicos = st.tabs(
    ["Produção", "Vacinação", "Pré-natal", "Visitas domiciliares", "Hipertensos/Diabéticos"]
)

with tab_producao:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Produção por UBS")
        fig = px.bar(
            producao_ubs_f, x="mes", y="total_atendimentos", color="no_unidade_saude", barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Produção por equipe")
        fig = px.bar(
            producao_equipe_f, x="mes", y="total_atendimentos", color="no_equipe", barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab_vacinal:
    st.subheader("Cobertura vacinal — doses aplicadas por mês/imunobiológico")
    fig = px.bar(vacinal, x="mes", y="doses_aplicadas", color="co_imunobiologico", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(vacinal, use_container_width=True)

with tab_pre_natal:
    st.subheader("Acompanhamento de pré-natal")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de gestações", int(pre_natal["total_gestacoes"].iloc[0]))
    c2.metric("Em andamento", int(pre_natal["gestacoes_em_andamento"].iloc[0]))
    c3.metric("Alto risco", int(pre_natal["gestacoes_alto_risco"].iloc[0]))
    c4.metric("Planejadas", int(pre_natal["gestacoes_planejadas"].iloc[0]))

with tab_visitas:
    st.subheader("Visitas domiciliares por equipe/mês")
    fig = px.bar(visitas_f, x="mes", y="total_visitas", color="no_equipe", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

with tab_cronicos:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Hipertensos por faixa etária")
        h = hipertensos.copy()
        h["faixa_etaria"] = pd.cut(h["idade"], bins=[0, 18, 30, 45, 60, 75, 120])
        fig = px.histogram(h, x="faixa_etaria", color="no_sexo", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Diabéticos por faixa etária")
        d = diabeticos.copy()
        d["faixa_etaria"] = pd.cut(d["idade"], bins=[0, 18, 30, 45, 60, 75, 120])
        fig = px.histogram(d, x="faixa_etaria", color="no_sexo", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

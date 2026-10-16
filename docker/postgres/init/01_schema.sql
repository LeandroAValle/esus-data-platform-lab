-- Schema sintético inspirado no e-SUS APS, apenas para fins de estudo/portfólio.
-- Dados sempre fictícios/anonimizados.

CREATE SCHEMA IF NOT EXISTS esus;

CREATE TABLE esus.ubs (
    id_ubs SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    municipio VARCHAR(120) NOT NULL,
    uf CHAR(2) NOT NULL
);

CREATE TABLE esus.equipe (
    id_equipe SERIAL PRIMARY KEY,
    id_ubs INT NOT NULL REFERENCES esus.ubs(id_ubs),
    nome_equipe VARCHAR(120) NOT NULL,
    tipo_equipe VARCHAR(50) NOT NULL DEFAULT 'ESF'
);

CREATE TABLE esus.profissional (
    id_profissional SERIAL PRIMARY KEY,
    id_equipe INT NOT NULL REFERENCES esus.equipe(id_equipe),
    nome VARCHAR(120) NOT NULL,
    cbo VARCHAR(20) NOT NULL,
    cargo VARCHAR(80) NOT NULL
);

CREATE TABLE esus.cidadao (
    id_cidadao SERIAL PRIMARY KEY,
    id_equipe INT REFERENCES esus.equipe(id_equipe),
    cpf_hash VARCHAR(64) NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) NOT NULL,
    is_gestante BOOLEAN NOT NULL DEFAULT FALSE,
    is_hipertenso BOOLEAN NOT NULL DEFAULT FALSE,
    is_diabetico BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE esus.atendimento (
    id_atendimento SERIAL PRIMARY KEY,
    id_cidadao INT NOT NULL REFERENCES esus.cidadao(id_cidadao),
    id_profissional INT NOT NULL REFERENCES esus.profissional(id_profissional),
    id_ubs INT NOT NULL REFERENCES esus.ubs(id_ubs),
    tipo_atendimento VARCHAR(50) NOT NULL, -- consulta, visita_domiciliar, pre_natal, etc.
    data_atendimento TIMESTAMP NOT NULL DEFAULT now(),
    observacoes TEXT
);

CREATE TABLE esus.vacina_aplicada (
    id_vacina_aplicada SERIAL PRIMARY KEY,
    id_cidadao INT NOT NULL REFERENCES esus.cidadao(id_cidadao),
    id_ubs INT NOT NULL REFERENCES esus.ubs(id_ubs),
    imunobiologico VARCHAR(80) NOT NULL,
    dose VARCHAR(30) NOT NULL,
    data_aplicacao DATE NOT NULL
);

CREATE TABLE esus.pre_natal (
    id_pre_natal SERIAL PRIMARY KEY,
    id_cidadao INT NOT NULL REFERENCES esus.cidadao(id_cidadao),
    data_inicio_pre_natal DATE NOT NULL,
    numero_consultas INT NOT NULL DEFAULT 0,
    risco VARCHAR(20) NOT NULL DEFAULT 'habitual' -- habitual, alto_risco
);

CREATE TABLE esus.meta_aps (
    id_meta SERIAL PRIMARY KEY,
    id_equipe INT NOT NULL REFERENCES esus.equipe(id_equipe),
    indicador VARCHAR(80) NOT NULL,
    periodo VARCHAR(7) NOT NULL, -- YYYY-MM
    valor_meta NUMERIC(10,2) NOT NULL,
    valor_realizado NUMERIC(10,2)
);

-- Dados sintéticos para validação do ambiente. Sem relação com pessoas reais.

INSERT INTO esus.ubs (nome, municipio, uf) VALUES
    ('UBS Jardim das Flores', 'Cidade Exemplo', 'SP'),
    ('UBS Vila Esperança', 'Cidade Exemplo', 'SP');

INSERT INTO esus.equipe (id_ubs, nome_equipe, tipo_equipe) VALUES
    (1, 'ESF 01', 'ESF'),
    (1, 'ESF 02', 'ESF'),
    (2, 'ESF 03', 'ESF');

INSERT INTO esus.profissional (id_equipe, nome, cbo, cargo) VALUES
    (1, 'Dra. Ana Souza', '225125', 'Médico'),
    (1, 'Enf. Bruno Lima', '223505', 'Enfermeiro'),
    (2, 'Dr. Carlos Melo', '225125', 'Médico'),
    (3, 'Enf. Diana Ramos', '223505', 'Enfermeiro');

INSERT INTO esus.cidadao (id_equipe, cpf_hash, data_nascimento, sexo, is_gestante, is_hipertenso, is_diabetico) VALUES
    (1, 'hash_0001', '1985-03-12', 'F', TRUE,  FALSE, FALSE),
    (1, 'hash_0002', '1958-07-01', 'M', FALSE, TRUE,  TRUE),
    (2, 'hash_0003', '1990-11-20', 'F', FALSE, FALSE, FALSE),
    (2, 'hash_0004', '1970-01-15', 'M', FALSE, TRUE,  FALSE),
    (3, 'hash_0005', '1995-05-30', 'F', TRUE,  FALSE, FALSE);

INSERT INTO esus.atendimento (id_cidadao, id_profissional, id_ubs, tipo_atendimento, data_atendimento) VALUES
    (1, 1, 1, 'pre_natal', now() - interval '30 days'),
    (2, 1, 1, 'consulta', now() - interval '20 days'),
    (2, 2, 1, 'visita_domiciliar', now() - interval '10 days'),
    (3, 3, 2, 'consulta', now() - interval '5 days'),
    (5, 4, 2, 'pre_natal', now() - interval '15 days');

INSERT INTO esus.vacina_aplicada (id_cidadao, id_ubs, imunobiologico, dose, data_aplicacao) VALUES
    (1, 1, 'dTpa', '1ª dose', now() - interval '25 days'),
    (3, 2, 'Influenza', 'dose única', now() - interval '40 days');

INSERT INTO esus.pre_natal (id_cidadao, data_inicio_pre_natal, numero_consultas, risco) VALUES
    (1, now() - interval '90 days', 3, 'habitual'),
    (5, now() - interval '45 days', 1, 'alto_risco');

INSERT INTO esus.meta_aps (id_equipe, indicador, periodo, valor_meta, valor_realizado) VALUES
    (1, 'cobertura_pre_natal', to_char(now(), 'YYYY-MM'), 90.00, 75.00),
    (1, 'cobertura_vacinal', to_char(now(), 'YYYY-MM'), 95.00, 80.00),
    (2, 'visitas_domiciliares', to_char(now(), 'YYYY-MM'), 100.00, 60.00);

# Publicação segura

Esta cópia pública foi preparada a partir **somente dos arquivos versionados** do laboratório local, com histórico Git novo. O arquivo `.env` real, dados em `data/raw/` e `data/lakehouse/`, exports, ambientes virtuais e logs não foram copiados.

Os exemplos de configuração foram generalizados. A stack Docker de demonstração exige senha definida em `docker/.env` e expõe Postgres, Adminer, Airflow e Streamlit apenas em `127.0.0.1` por padrão nesta cópia. O socket Docker montado no Airflow oferece controle elevado do host; execute a stack somente em ambiente de laboratório confiável.

Hash com salt de CPF/CNS e remoção de campos diretos reduzem exposição, mas **não tornam automaticamente anônimos** conjuntos de saúde. Campos clínicos e combinações indiretas podem permitir reidentificação. O código é para aprendizado e precisa de revisão técnica e jurídica antes de uso com dados reais.

O site `site/` lê apenas `layers.json`, que contém nomes de camadas, tecnologias e caminhos de arquivos. Nenhuma métrica operacional ou registro pessoal é publicado.

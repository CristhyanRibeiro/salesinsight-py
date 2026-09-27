# SalesInsight PY

Mini-Projeto Avaliativo do Módulo 01 do curso de Desenvolvimento de IA para Análise Preditiva - SCTEC/SENAI.

## Objetivo

Desenvolver uma aplicação em Python para análise de dados de vendas, utilizando os conteúdos estudados até a Semana 05.

## Funcionalidades

O projeto realiza:

- geração de um dataset sintético de vendas;
- leitura de arquivo CSV;
- inspeção dos dados;
- identificação de valores ausentes;
- limpeza e padronização dos dados;
- tratamento de datas inválidas;
- uso de expressões regulares;
- criação de colunas derivadas;
- cálculo de métricas de vendas;
- análise por produto, categoria e região;
- segmentação de clientes em Bronze, Prata e Ouro;
- uso de funções lambda;
- exportação de resultados em CSV e JSON.

## Tecnologias utilizadas

- Python
- csv
- json
- datetime
- re
- os
- random

Foram utilizadas apenas bibliotecas padrão do Python.

## Estrutura do projeto

```text
salesinsight-py/
├── outputs/
│   ├── estatisticas_gerais.json
│   ├── metricas_por_mes.csv
│   └── segmentacao_clientes.csv
├── README.md
├── salesinsight.py
└── vendas.csv

## Autor

Cristhyan Allan Ribeiro  
Curso de Desenvolvimento de IA para Análise Preditiva  
Programa SCTEC - SENAI/SC
"""
SalesInsight PY - Analise de Dados de Vendas
Mini-Projeto Avaliativo - Modulo 01
"""

import re
import csv
import random
from datetime import datetime, timedelta


def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos e grava em CSV."""

    random.seed(seed)

    produtos = [
        "Notebook", "Smartphone", "Tablet", "Monitor",
        "Teclado", "Mouse", "Headset"
    ]

    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Perifericos",
        "Mouse": "Perifericos",
        "Headset": "Perifericos"
    }

    precos = {
        "Notebook": 3500,
        "Smartphone": 2200,
        "Tablet": 1800,
        "Monitor": 1200,
        "Teclado": 250,
        "Mouse": 120,
        "Headset": 350
    }

    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    data_inicio = datetime(2025, 1, 1)

    colunas = [
        "id_venda",
        "data_venda",
        "cliente",
        "produto",
        "categoria",
        "regiao",
        "quantidade",
        "preco_unitario"
    ]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            # Sujeira proposital para a etapa de limpeza
            if random.random() < 0.05:
                quantidade = ""

            if random.random() < 0.04:
                preco = ""

            if random.random() < 0.06:
                produto = " " + produto + " "

            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"

            if random.random() < 0.10:
                cliente = random.choice([
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#")
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco
            })

    print(f"Dataset gerado com {n_registros} registros em {caminho_csv}.")

def carregar_dataset(caminho_csv):
    """Le o CSV e retorna uma lista de dicionarios."""

    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        registros = list(leitor)

    return registros


def inspecionar_dados(registros):
    """Exibe as informacoes principais do dataset."""

    total = len(registros)

    if registros:
        colunas = list(registros[0].keys())
    else:
        colunas = []

    nulos = {}

    for coluna in colunas:
        nulos[coluna] = 0

    for linha in registros:
        for coluna in colunas:
            if linha[coluna].strip() == "":
                nulos[coluna] += 1

    print("\n=== INSPECAO INICIAL ===")
    print("Total de registros:", total)
    print("Colunas:", colunas)
    print("Valores ausentes:", nulos)

    print("\nPrimeiros registros:")

    for linha in registros[:5]:
        print(linha)

    return registros

def limpar_dados(registros):
    """Limpa os registros e remove dados invalidos."""

    relatorio = {
        "iniciais": len(registros),
        "removidos_data": 0,
        "removidos_nulos": 0,
        "finais": 0
    }

    limpos = []
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", re.IGNORECASE)

    for linha in registros:

        # Remove espacos extras
        linha["cliente"] = linha["cliente"].strip()
        linha["produto"] = linha["produto"].strip()
        linha["categoria"] = linha["categoria"].strip()
        linha["regiao"] = linha["regiao"].strip()

        # Verifica a data
        try:
            linha["data_venda"] = datetime.strptime(
                linha["data_venda"], "%Y-%m-%d"
            )
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        # Verifica valores ausentes
        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

        # Converte os tipos numericos
        linha["quantidade"] = int(linha["quantidade"])
        linha["preco_unitario"] = float(linha["preco_unitario"])

        # Limpa o nome do cliente
        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])

        # Padroniza casos como cliente016 para Cliente_016
        numeros = re.sub(r"[^0-9]", "", nome_limpo)

        if len(numeros) == 3:
            nome_limpo = "Cliente_" + numeros

        linha["cliente"] = nome_limpo

        # Verifica se ficou fora do padrao
        if padrao_cliente.match(nome_limpo):
            linha["cliente_fora_do_padrao"] = False
        else:
            linha["cliente_fora_do_padrao"] = True

        limpos.append(linha)

    relatorio["finais"] = len(limpos)

    print("\n=== RELATORIO DE LIMPEZA ===")
    print("Registros iniciais:", relatorio["iniciais"])
    print("Removidos por data invalida:", relatorio["removidos_data"])
    print("Removidos por valores ausentes:", relatorio["removidos_nulos"])
    print("Registros finais:", relatorio["finais"])

    return limpos, relatorio


gerar_dataset_vendas()

registros = carregar_dataset("vendas.csv")
inspecionar_dados(registros)
registros_limpos, relatorio = limpar_dados(registros)
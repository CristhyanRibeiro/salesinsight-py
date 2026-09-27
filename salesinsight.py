"""
SalesInsight PY - Analise de Dados de Vendas
Mini-Projeto Avaliativo - Modulo 01
"""

import csv
import json
import os
import random
import re
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

    regioes = [
        "Sudeste",
        "Sul",
        "Nordeste",
        "Centro-Oeste",
        "Norte"
    ]

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
            preco = round(
                precos[produto] * random.uniform(0.85, 1.15),
                2
            )

            data = data_inicio + timedelta(
                days=random.randint(0, 364)
            )

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

    print(
        f"Dataset gerado com {n_registros} registros em {caminho_csv}."
    )


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

    padrao_cliente = re.compile(
        r"^Cliente_\d{3}$",
        re.IGNORECASE
    )

    for linha in registros:

        # Remove espacos extras
        linha["cliente"] = linha["cliente"].strip()
        linha["produto"] = linha["produto"].strip()
        linha["categoria"] = linha["categoria"].strip()
        linha["regiao"] = linha["regiao"].strip()

        # Verifica a data
        try:
            linha["data_venda"] = datetime.strptime(
                linha["data_venda"],
                "%Y-%m-%d"
            )
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        # Verifica valores ausentes
        if (
            linha["quantidade"] == ""
            or linha["preco_unitario"] == ""
        ):
            relatorio["removidos_nulos"] += 1
            continue

        # Converte os tipos numericos
        linha["quantidade"] = int(linha["quantidade"])
        linha["preco_unitario"] = float(
            linha["preco_unitario"]
        )

        # Limpa o nome do cliente
        nome_limpo = re.sub(
            r"[^A-Za-z0-9_]",
            "",
            linha["cliente"]
        )

        numeros = re.sub(
            r"[^0-9]",
            "",
            nome_limpo
        )

        if len(numeros) == 3:
            nome_limpo = "Cliente_" + numeros

        linha["cliente"] = nome_limpo

        # Verifica o padrao do cliente
        if padrao_cliente.match(nome_limpo):
            linha["cliente_fora_do_padrao"] = False
        else:
            linha["cliente_fora_do_padrao"] = True

        limpos.append(linha)

    relatorio["finais"] = len(limpos)

    print("\n=== RELATORIO DE LIMPEZA ===")
    print(
        "Registros iniciais:",
        relatorio["iniciais"]
    )
    print(
        "Removidos por data invalida:",
        relatorio["removidos_data"]
    )
    print(
        "Removidos por valores ausentes:",
        relatorio["removidos_nulos"]
    )
    print(
        "Registros finais:",
        relatorio["finais"]
    )

    return limpos, relatorio


def criar_colunas_derivadas(registros):
    """Cria novas informacoes a partir dos dados de vendas."""

    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Marco",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    for linha in registros:

        # Receita da venda
        linha["receita_total"] = (
            linha["quantidade"]
            * linha["preco_unitario"]
        )

        # Mes e ano
        mes = linha["data_venda"].month

        linha["mes"] = mes
        linha["mes_nome"] = meses[mes]
        linha["ano"] = linha["data_venda"].year

        # Trimestre
        if mes <= 3:
            linha["trimestre"] = "Q1"
        elif mes <= 6:
            linha["trimestre"] = "Q2"
        elif mes <= 9:
            linha["trimestre"] = "Q3"
        else:
            linha["trimestre"] = "Q4"

        # Faixa de receita
        if linha["receita_total"] < 500:
            linha["faixa_receita_item"] = "Baixo Valor"
        elif linha["receita_total"] < 5000:
            linha["faixa_receita_item"] = "Medio Valor"
        else:
            linha["faixa_receita_item"] = "Alto Valor"

    return registros


def calcular_metricas(registros):
    """Calcula metricas de vendas."""

    por_mes = {}
    por_produto = {}
    por_categoria = {}
    por_regiao = {}

    for linha in registros:
        mes = linha["mes_nome"]
        produto = linha["produto"]
        categoria = linha["categoria"]
        regiao = linha["regiao"]
        receita = linha["receita_total"]
        quantidade = linha["quantidade"]

        # Metricas por mes
        if mes not in por_mes:
            por_mes[mes] = {
                "receita": 0,
                "quantidade": 0,
                "vendas": 0
            }

        por_mes[mes]["receita"] += receita
        por_mes[mes]["quantidade"] += quantidade
        por_mes[mes]["vendas"] += 1

        # Metricas por produto
        if produto not in por_produto:
            por_produto[produto] = {
                "receita": 0,
                "quantidade": 0,
                "vendas": 0
            }

        por_produto[produto]["receita"] += receita
        por_produto[produto]["quantidade"] += quantidade
        por_produto[produto]["vendas"] += 1

        # Metricas por categoria
        if categoria not in por_categoria:
            por_categoria[categoria] = {
                "receita": 0,
                "quantidade": 0,
                "vendas": 0
            }

        por_categoria[categoria]["receita"] += receita
        por_categoria[categoria]["quantidade"] += quantidade
        por_categoria[categoria]["vendas"] += 1

        # Metricas por regiao
        if regiao not in por_regiao:
            por_regiao[regiao] = {
                "receita": 0,
                "quantidade": 0,
                "vendas": 0
            }

        por_regiao[regiao]["receita"] += receita
        por_regiao[regiao]["quantidade"] += quantidade
        por_regiao[regiao]["vendas"] += 1

    # Ticket medio mensal
    for mes in por_mes:
        por_mes[mes]["ticket_medio"] = (
            por_mes[mes]["receita"]
            / por_mes[mes]["vendas"]
        )

    metricas = {
        "por_mes": por_mes,
        "por_produto": por_produto,
        "por_categoria": por_categoria,
        "por_regiao": por_regiao
    }

    return metricas


def segmentar_clientes(registros):
    """Classifica clientes em Bronze, Prata ou Ouro."""

    clientes = {}

    for linha in registros:
        cliente = linha["cliente"]
        receita = linha["receita_total"]

        if cliente not in clientes:
            clientes[cliente] = 0

        clientes[cliente] += receita

    # Primeiro uso de lambda
    classificar = lambda total: (
        "Bronze" if total < 5000
        else "Prata" if total < 15000
        else "Ouro"
    )

    segmentacao = []

    for cliente in clientes:
        total = clientes[cliente]

        segmentacao.append({
            "cliente": cliente,
            "total_compras": round(total, 2),
            "segmento": classificar(total)
        })

    # Segundo uso de lambda
    segmentacao.sort(
        key=lambda item: item["total_compras"],
        reverse=True
    )

    return segmentacao


def aplicar_operacao(registros, funcao):
    """Recebe uma funcao como argumento."""
    return funcao(registros)


def calcular_receita_total(registros):
    """Calcula a receita total das vendas."""

    total = 0

    for linha in registros:
        total += linha["receita_total"]

    return total


def exportar_resultados(metricas, segmentacao, registros):
    """Exporta os resultados para CSV e JSON."""

    os.makedirs("outputs", exist_ok=True)

    # Metricas por mes
    with open(
        "outputs/metricas_por_mes.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        colunas = [
            "mes",
            "receita",
            "quantidade",
            "vendas",
            "ticket_medio"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )

        escritor.writeheader()

        for mes in metricas["por_mes"]:
            dados = metricas["por_mes"][mes]

            escritor.writerow({
                "mes": mes,
                "receita": round(
                    dados["receita"],
                    2
                ),
                "quantidade": dados["quantidade"],
                "vendas": dados["vendas"],
                "ticket_medio": round(
                    dados["ticket_medio"],
                    2
                )
            })

    # Segmentacao dos clientes
    with open(
        "outputs/segmentacao_clientes.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        colunas = [
            "cliente",
            "total_compras",
            "segmento"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )

        escritor.writeheader()

        for cliente in segmentacao:
            escritor.writerow({
                "cliente": cliente["cliente"],
                "total_compras": cliente["total_compras"],
                "segmento": cliente["segmento"]
            })

    # Estatisticas gerais
    receita_total = calcular_receita_total(registros)

    estatisticas = {
        "total_registros": len(registros),
        "receita_total": round(receita_total, 2),
        "total_clientes": len(segmentacao)
    }

    with open(
        "outputs/estatisticas_gerais.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            estatisticas,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print("\nArquivos exportados com sucesso.")


def ler_json_resultados():
    """Le o arquivo JSON exportado e exibe seu conteudo."""

    with open(
        "outputs/estatisticas_gerais.json",
        "r",
        encoding="utf-8"
    ) as arquivo:
        dados = json.load(arquivo)

    print("\n=== ESTATISTICAS GERAIS ===")
    print(dados)


def main():
    """Executa todas as etapas do projeto."""

    print("=" * 50)
    print("SALESINSIGHT PY - ANALISE DE VENDAS")
    print("=" * 50)

    # 1. Gera o dataset
    gerar_dataset_vendas()

    # 2. Carrega e inspeciona
    registros = carregar_dataset("vendas.csv")
    inspecionar_dados(registros)

    # 3. Limpa os dados
    registros_limpos, relatorio = limpar_dados(registros)

    # 4. Cria as colunas derivadas
    registros_limpos = criar_colunas_derivadas(
        registros_limpos
    )

    # 5. Calcula as metricas
    metricas = calcular_metricas(registros_limpos)

    print("\n=== METRICAS POR PRODUTO ===")

    for produto in metricas["por_produto"]:
        print(
            produto,
            metricas["por_produto"][produto]
        )

    print("\n=== METRICAS POR CATEGORIA ===")

    for categoria in metricas["por_categoria"]:
        print(
            categoria,
            metricas["por_categoria"][categoria]
        )

    print("\n=== METRICAS POR REGIAO ===")

    for regiao in metricas["por_regiao"]:
        print(
            regiao,
            metricas["por_regiao"][regiao]
        )

    # 6. Segmenta os clientes
    segmentacao = segmentar_clientes(
        registros_limpos
    )

    # 7. Demonstra funcao recebendo outra funcao
    receita_total = aplicar_operacao(
        registros_limpos,
        calcular_receita_total
    )

    # 8. Exibe resumo
    print("\n=== RESUMO ===")
    print(
        "Receita total: R$",
        round(receita_total, 2)
    )

    print("\n=== TOP 5 CLIENTES ===")

    for cliente in segmentacao[:5]:
        print(cliente)

    # 9. Exporta os resultados
    exportar_resultados(
        metricas,
        segmentacao,
        registros_limpos
    )

    # 10. Le o JSON exportado
    ler_json_resultados()


if __name__ == "__main__":
    main()
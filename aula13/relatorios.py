"""A13 — registro e exportação de vendas em CSV."""

import csv
from datetime import datetime
from pathlib import Path


COLUNAS_VENDAS = (
    "data_hora",
    "forma_pagamento",
    "total_centavos",
    "total_reais",
)


def _linha_venda(comprovante):
    centavos = int(comprovante.total_centavos)

    return (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        comprovante.forma,
        centavos,
        f"{centavos // 100}.{centavos % 100:02d}",
    )


def exportar_csv(caminho, comprovante):
    """Cria ou substitui um CSV com o cabeçalho e uma venda."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(COLUNAS_VENDAS)
        escritor.writerow(_linha_venda(comprovante))


def registrar_venda_csv(comprovante, arquivo="vendas.csv"):
    """Acrescenta uma venda ao arquivo, criando o cabeçalho quando necessário."""
    caminho = Path(arquivo)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    precisa_cabecalho = not caminho.exists() or caminho.stat().st_size == 0

    with caminho.open("a", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.writer(arquivo_csv, delimiter=";")

        if precisa_cabecalho:
            escritor.writerow(COLUNAS_VENDAS)

        escritor.writerow(_linha_venda(comprovante))

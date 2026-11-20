import csv
from datetime import datetime
from pathlib import Path


COLUNAS = ("data_hora", "forma_pagamento", "total_centavos", "total_reais")


def registrar_venda_csv(comprovante, caminho):
    caminho = Path(caminho)
    inteiro, centavos = divmod(comprovante.total_pago_centavos, 100)
    with caminho.open("a+", encoding="utf-8", newline="") as arquivo:
        arquivo.seek(0)
        leitor = csv.reader(arquivo, delimiter=";")
        cabecalho = next(leitor, None)
        if cabecalho is not None and cabecalho != list(COLUNAS):
            raise ValueError("Cabeçalho do arquivo vendas.csv inválido.")
        arquivo.seek(0, 2)
        escritor = csv.writer(arquivo, delimiter=";")
        if cabecalho is None:
            escritor.writerow(COLUNAS)
        escritor.writerow((
            datetime.now().isoformat(sep=" ", timespec="seconds"),
            comprovante.forma,
            comprovante.total_pago_centavos,
            f"{inteiro},{centavos:02d}",
        ))

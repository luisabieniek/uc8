import csv
from pathlib import Path
from datetime import datetime

COLUNAS_VENDAS = ('data_hora', 'forma_pagamento', 'total_centavos', 'total_reais')


def _linha_venda(comprovante):
    return [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), comprovante.forma,
            comprovante.total_centavos, f'{comprovante.total_centavos / 100:.2f}']


def exportar_csv(caminho, comprovante):
    caminho = Path(caminho)
    with caminho.open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(COLUNAS_VENDAS)
        escritor.writerow(_linha_venda(comprovante))


def registrar_venda_csv(comprovante, arquivo='vendas.csv'):
    caminho = Path(arquivo)
    novo = not caminho.exists() or caminho.stat().st_size == 0
    with caminho.open('a', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv, delimiter=';')
        if novo:
            escritor.writerow(COLUNAS_VENDAS)
        escritor.writerow(_linha_venda(comprovante))

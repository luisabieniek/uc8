"""A13 — testes básicos dos módulos do sistema da pizzaria."""

import csv
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from arquivos import ler_catalogo, salvar_catalogo, validar_catalogo
from modelos import Pedido, Produto, formatar
from pagamento import FATORES, calcular_pagamento
from perfis import SessaoDemo
from relatorios import COLUNAS_VENDAS, exportar_csv, registrar_venda_csv


def verificar_catalogo_json():
    dados = [
        {"id": "P01", "nome": "Pizza", "preco_centavos": 4500},
    ]

    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "catalogo.json"
        salvar_catalogo(caminho, dados)
        assert ler_catalogo(caminho) == dados

    try:
        validar_catalogo([
            {"id": "P01", "nome": "Pizza", "preco_centavos": 4500},
            {"id": "P01", "nome": "Outra", "preco_centavos": 5000},
        ])
    except ValueError:
        pass
    else:
        raise AssertionError("O catálogo deveria recusar IDs duplicados.")


def verificar_pedido():
    pizza = Produto("P01", "Pizza", 4500)
    pedido = Pedido()

    pedido.adicionar(pizza, "2")
    assert pedido.total_centavos() == 9000

    pedido.atualizar("P01", "3")
    assert pedido.total_centavos() == 13500

    pedido.remover("P01")
    assert pedido.total_centavos() == 0

    pedido.adicionar(pizza, "2")
    versao = pedido.versao()
    comprovante = pedido.finalizar("Pix", versao)

    esperado, desconto = calcular_pagamento("90.00", "Pix")
    assert comprovante.total_centavos == esperado
    assert comprovante.desconto_centavos == desconto
    assert len(comprovante.linhas) == 1

    try:
        pedido.adicionar(pizza, "1")
    except RuntimeError:
        pass
    else:
        raise AssertionError("Não deveria permitir alterar pedido finalizado.")

    pedido.novo()
    assert pedido.itens == []


def verificar_pagamento_decimal():
    total, desconto = calcular_pagamento("100,00", "Pix")
    assert total == 9500
    assert desconto == 500
    assert set(FATORES) == {"Dinheiro", "Pix", "Débito", "Crédito"}


def verificar_csv():
    comprovante = SimpleNamespace(
        forma="Pix",
        total_centavos=12345,
    )

    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "vendas.csv"
        registrar_venda_csv(comprovante, caminho)
        registrar_venda_csv(comprovante, caminho)

        with caminho.open(newline="", encoding="utf-8") as arquivo:
            linhas = list(csv.reader(arquivo, delimiter=";"))

        assert tuple(linhas[0]) == COLUNAS_VENDAS
        assert len(linhas) == 3
        assert linhas[1][2:] == ["12345", "123.45"]

        exportado = Path(pasta) / "exportado.csv"
        exportar_csv(exportado, comprovante)
        assert exportado.exists()


def verificar_perfis():
    sessao = SessaoDemo()
    sessao.entrar("Luisa", "Caixa")
    assert sessao.pode_operar_vendas()
    assert not sessao.pode_configurar()

    sessao.entrar("Admin", "Administracao")
    assert sessao.pode_configurar()
    assert not sessao.pode_operar_vendas()

    sessao.sair()
    assert sessao.nome is None
    assert sessao.perfil is None


if __name__ == "__main__":
    testes = (
        ("Catálogo JSON", verificar_catalogo_json),
        ("Pedido", verificar_pedido),
        ("Pagamento Decimal", verificar_pagamento_decimal),
        ("Relatórios CSV", verificar_csv),
        ("Perfis", verificar_perfis),
    )

    for nome, teste in testes:
        teste()
        print(f"OK: {nome}")

    print(f"{len(testes)} verificações concluídas.")

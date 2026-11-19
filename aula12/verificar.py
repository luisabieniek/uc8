
"""A12 — testes do catálogo e da preservação do pedido."""

import json
import tempfile
from pathlib import Path

from arquivos import ler_catalogo, salvar_catalogo, validar_catalogo
from modelos import Pedido, Produto


CATALOGO_VALIDO = [
    {"id": 1, "nome": "Arroz", "preco_centavos": 2590},
    {"id": 2, "nome": "Feijão", "preco_centavos": 890},
    {"id": 3, "nome": "Macarrão", "preco_centavos": 650}
]


def esperar_erro(acao, mensagem=None):
    try:
        acao()
    except ValueError as erro:
        if mensagem is not None:
            assert mensagem in str(erro)
    else:
        raise AssertionError("Era esperado um ValueError.")


def estado_pedido(pedido):
    itens = []

    for item in pedido.itens:
        itens.append((
            item.produto.codigo,
            item.produto.nome,
            item.quantidade,
            item.subtotal()
        ))

    return (
        pedido.versao(),
        itens,
        pedido.total_centavos(),
        pedido.aberto
    )


def verificar_catalogo():
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "catalogo.json"

        # Arquivo ausente
        assert ler_catalogo(caminho) is None
        print("[OK] Catálogo ausente")

        # Salvar e ler catálogo válido
        salvar_catalogo(caminho, CATALOGO_VALIDO)

        conteudo_anterior = caminho.read_bytes()

        assert ler_catalogo(caminho) == CATALOGO_VALIDO
        assert caminho.read_bytes() == conteudo_anterior

        print("[OK] Catálogo válido e leitura sem alteração")

        # JSON inválido
        caminho.write_text(
            '[{"id": 1, "nome": "Arroz"',
            encoding="utf-8"
        )

        conteudo_invalido = caminho.read_bytes()

        esperar_erro(
            lambda: ler_catalogo(caminho),
            "JSON inválido"
        )

        assert caminho.read_bytes() == conteudo_invalido

        print("[OK] JSON inválido rejeitado e preservado")

        # Estrutura inválida
        estrutura = {
            "id": 1,
            "nome": "Arroz",
            "preco_centavos": 100
        }

        caminho.write_text(
            json.dumps(estrutura),
            encoding="utf-8"
        )

        conteudo_invalido = caminho.read_bytes()

        esperar_erro(
            lambda: ler_catalogo(caminho),
            "Catálogo deve ser uma lista"
        )

        assert caminho.read_bytes() == conteudo_invalido

        print("[OK] Estrutura inválida rejeitada")

        # IDs repetidos
        salvar_catalogo(caminho, CATALOGO_VALIDO)

        conteudo_anterior = caminho.read_bytes()

        catalogo_repetido = [
            {"id": 7, "nome": "Produto A", "preco_centavos": 100},
            {"id": "7", "nome": "Produto B", "preco_centavos": 200}
        ]

        esperar_erro(
            lambda: validar_catalogo(catalogo_repetido),
            "ID repetido"
        )

        esperar_erro(
            lambda: salvar_catalogo(caminho, catalogo_repetido),
            "ID repetido"
        )

        assert caminho.read_bytes() == conteudo_anterior

        print("[OK] ID repetido rejeitado sem alterar o arquivo")

        # Preço inválido
        catalogo_preco_invalido = [
            {"id": 1, "nome": "Arroz", "preco_centavos": 0}
        ]

        esperar_erro(
            lambda: validar_catalogo(catalogo_preco_invalido),
            "preço deve ser inteiro positivo"
        )

        assert caminho.read_bytes() == conteudo_anterior

        print("[OK] Preço inválido rejeitado")

    return True


def verificar_navegacao():
    arroz = Produto("1", "Arroz", 2590)
    feijao = Produto("2", "Feijão", 890)

    pedido = Pedido()
    pedido.adicionar(arroz, "2")

    estado_inicial = estado_pedido(pedido)

    # Simula carregar outro catálogo
    catalogo_novo = [
        {"id": 10, "nome": "Suco", "preco_centavos": 600}
    ]

    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "outro_catalogo.json"

        salvar_catalogo(caminho, catalogo_novo)

        dados = ler_catalogo(caminho)

        assert dados == catalogo_novo

    assert estado_pedido(pedido) == estado_inicial

    print("[OK] Troca de catálogo preservou o pedido")

    # Entrada inválida não pode alterar o pedido
    esperar_erro(
        lambda: pedido.adicionar(feijao, "abc")
    )

    assert estado_pedido(pedido) == estado_inicial

    print("[OK] Quantidade inválida preservou o pedido")

    # Prévia desatualizada não pode finalizar
    esperar_erro(
        lambda: pedido.finalizar(
            "PIX",
            pedido.versao() + 99
        ),
        "pedido foi alterado"
    )

    assert estado_pedido(pedido) == estado_inicial

    print("[OK] Prévia desatualizada preservou o pedido")

    # Testa o valor correto
    assert pedido.total_centavos() == 5180
    assert estado_pedido(pedido) == estado_inicial

    print("[OK] Total do pedido conferido")

    return True


def executar_testes():
    verificar_catalogo()
    verificar_navegacao()

    print("\nTodos os testes foram executados com sucesso!")


if __name__ == "__main__":
    executar_testes()

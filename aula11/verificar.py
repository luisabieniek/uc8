from modelos import Pizza, Bebida, Pedido
from pagamento import calcular_pagamento
from decimal import Decimal


def verificar_adicionar():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 2)

    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 2
    assert pedido.calcular_total() == 7000


def verificar_atualizar():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 1)
    pedido.atualizar("P01", 3)

    assert pedido.itens[0].quantidade == 3
    assert pedido.calcular_total() == 10500


def verificar_remover():
    pedido = Pedido()
    bebida = Bebida("B01", "Refrigerante", 600)

    pedido.adicionar(bebida, 2)
    pedido.remover("B01")

    assert len(pedido.itens) == 0
    assert pedido.calcular_total() == 0


def verificar_quantidade_invalida():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    try:
        pedido.adicionar(pizza, 0)
        assert False
    except ValueError:
        assert len(pedido.itens) == 0


def verificar_pagamento():
    resultado = calcular_pagamento(10000, "PIX")

    assert resultado["forma"] == "PIX"
    assert resultado["valor_final"] == 87


def verificar_cancelamento_da_previa():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 1)

    versao_previa = pedido.versao()

    # Simula o cancelamento: não chama finalizar.
    assert pedido.aberto is True
    assert pedido.calcular_total() == 3500
    assert pedido.versao() == versao_previa


def verificar_previa_desatualizada():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)
    bebida = Bebida("B01", "Refrigerante", 600)

    pedido.adicionar(pizza, 1)
    versao_previa = pedido.versao()

    pedido.adicionar(bebida, 1)

    try:
        pedido.finalizar("PIX", versao_previa)
        assert False
    except ValueError:
        assert pedido.aberto is True


def verificar_confirmar_pedido():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 1)

    comprovante = pedido.finalizar(
        "PIX",
        pedido.versao()
    )

    assert pedido.aberto is False
    assert comprovante.pagamento["forma"] == "PIX"
    assert comprovante.pagamento["valor_final"] == Decimal("30.45")


def verificar_nao_finalizar_duas_vezes():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 1)
    pedido.finalizar("PIX", pedido.versao())

    try:
        pedido.finalizar("PIX", pedido.versao())
        assert False
    except ValueError:
        assert pedido.aberto is False


def verificar_comprovante_independente():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 1)

    comprovante = pedido.finalizar(
        "Dinheiro",
        pedido.versao()
    )

    nome_comprovante = comprovante.itens[0]["nome"]

    assert nome_comprovante == "Mussarela"
    assert comprovante.itens[0]["quantidade"] == 1


def verificar_novo_pedido():
    pedido = Pedido()
    pizza = Pizza("P01", "Mussarela", "Média", 3500)

    pedido.adicionar(pizza, 1)
    pedido.novo()

    assert pedido.aberto is True
    assert len(pedido.itens) == 0
    assert pedido.calcular_total() == 0


def executar_testes():
    verificar_adicionar()
    verificar_atualizar()
    verificar_remover()
    verificar_quantidade_invalida()
    verificar_pagamento()
    verificar_cancelamento_da_previa()
    verificar_previa_desatualizada()
    verificar_confirmar_pedido()
    verificar_nao_finalizar_duas_vezes()
    verificar_comprovante_independente()
    verificar_novo_pedido()

    print("Todos os testes foram executados com sucesso!")


if __name__ == "__main__":
    executar_testes()
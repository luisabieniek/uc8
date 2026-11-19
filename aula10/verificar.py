
from modelos import Pizza, Bebida, Produto, Pedido, formatar
from pagamentos import calcular_pagamento
from decimal import Decimal


def verificar_caso_principal():
    mussarela = Pizza("P01", "Mussarela", "Media", 3500)
    bebida = Bebida("B01", "Suco", 600)

    pedido = Pedido()

    pedido.adicionar(mussarela, "1")
    pedido.adicionar(bebida, "2")

    assert pedido.total_centavos() == 4700
    assert formatar(4700) == "R$ 47,00"
    assert len(pedido.itens) == 2
    assert pedido.itens[0].subtotal() == 3500
    assert pedido.itens[1].subtotal() == 1200

    return True


def verificar_pizza():
    pizza = Pizza("P02", "Calabresa", "Grande", 4200)

    assert pizza.codigo == "P02"
    assert pizza.nome == "Calabresa"
    assert pizza.tamanho == "Grande"
    assert pizza.preco_centavos == 4200

    try:
        Pizza("P03", "Frango", "Gigante", 3000)
        assert False
    except ValueError:
        pass

    try:
        Pizza("", "Frango", "Media", 3000)
        assert False
    except ValueError:
        pass

    try:
        Pizza("P04", "Frango", "Media", 0)
        assert False
    except ValueError:
        pass

    return True


def verificar_bebida():
    bebida = Bebida("B02", "Refrigerante", 500)

    assert bebida.codigo == "B02"
    assert bebida.nome == "Refrigerante"
    assert bebida.preco_centavos == 500

    try:
        Bebida("B03", "", 500)
        assert False
    except ValueError:
        pass

    return True


def verificar_pedido_preservado_em_erro():
    mussarela = Pizza("P01", "Mussarela", "Media", 3500)
    bebida = Bebida("B01", "Suco", 600)

    pedido = Pedido()

    pedido.adicionar(mussarela, "1")
    pedido.adicionar(bebida, "2")

    total_anterior = pedido.total_centavos()
    itens_anteriores = len(pedido.itens)
    quantidades_anteriores = [item.quantidade for item in pedido.itens]

    try:
        pedido.atualizar("P01", "0")
        assert False
    except ValueError:
        pass

    assert pedido.total_centavos() == total_anterior
    assert len(pedido.itens) == itens_anteriores
    assert [item.quantidade for item in pedido.itens] == quantidades_anteriores

    try:
        pedido.atualizar("X99", "1")
        assert False
    except ValueError:
        pass

    assert pedido.total_centavos() == total_anterior

    try:
        pedido.remover("X99")
        assert False
    except ValueError:
        pass

    assert len(pedido.itens) == itens_anteriores

    return True


def verificar_item_aceita_qualquer_produto():
    generico = Produto("G01", "Generico", 100)
    pizza = Pizza("P01", "Mussarela", "Media", 3500)
    bebida = Bebida("B01", "Suco", 600)

    pedido = Pedido()

    pedido.adicionar(generico, "1")
    pedido.adicionar(pizza, "1")
    pedido.adicionar(bebida, "1")

    assert pedido.total_centavos() == 4200
    assert len(pedido.itens) == 3

    return True


def verificar_previa_falsa():
    mussarela = Pizza("P01", "Mussarela", "Media", 3500)
    bebida = Bebida("B01", "Suco", 600)

    pedido = Pedido()

    pedido.adicionar(mussarela, "1")
    pedido.adicionar(bebida, "2")

    previa_falsa_falhou = False

    try:
        assert pedido.total_centavos() == 9999
    except AssertionError:
        previa_falsa_falhou = True

    assert previa_falsa_falhou

    assert pedido.total_centavos() == 4700
    assert len(pedido.itens) == 2

    return True


def verificar_transferencia():
    frango = Pizza("P10", "Frango", "Grande", 4500)
    refrigerante = Bebida("B10", "Refri", 500)

    pedido = Pedido()

    pedido.adicionar(frango, "1")
    pedido.adicionar(refrigerante, "3")

    assert pedido.total_centavos() == 6000
    assert pedido.itens[0].subtotal() == 4500
    assert pedido.itens[1].subtotal() == 1500
    assert formatar(6000) == "R$ 60,00"

    assert pedido.itens[0].produto.codigo == "P10"
    assert pedido.itens[0].produto.preco_centavos == 4500
    assert pedido.itens[1].produto.codigo == "B10"
    assert pedido.itens[1].produto.preco_centavos == 500

    previa_falsa_falhou = False

    try:
        assert pedido.total_centavos() == 9999
    except AssertionError:
        previa_falsa_falhou = True

    assert previa_falsa_falhou

    assert pedido.total_centavos() == 6000
    assert len(pedido.itens) == 2

    pedido.atualizar("P10", "2")

    assert pedido.itens[0].quantidade == 2
    assert pedido.total_centavos() == 10500
    assert pedido.itens[1].quantidade == 3

    pedido.remover("B10")

    assert len(pedido.itens) == 1
    assert pedido.total_centavos() == 9000

    pedido.remover("P10")

    assert len(pedido.itens) == 0
    assert pedido.total_centavos() == 0

    return True


def verificar_pagamento_regressao():
    assert calcular_pagamento("100,00", "Dinheiro") == (8700, 1300)
    assert calcular_pagamento("100,00", "PIX") == (8700, 1300)
    assert calcular_pagamento("100,00", "Débito") == (9200, 800)
    assert calcular_pagamento("100,00", "Crédito 1x") == (10000, 0)

    assert calcular_pagamento("0,50", "PIX") == (44, 6)

    assert calcular_pagamento("100,00", "PIX") == (8700, 1300)
    assert calcular_pagamento("100,00", "PIX") == (8700, 1300)

    try:
        calcular_pagamento("100,00", "Boleto")
        assert False
    except ValueError:
        pass

    mussarela = Pizza("P01", "Mussarela", "Media", 3500)
    bebida = Bebida("B01", "Suco", 600)

    pedido = Pedido()

    pedido.adicionar(mussarela, "1")
    pedido.adicionar(bebida, "2")

    subtotal = str(Decimal(pedido.total_centavos()) / 100)

    total, desconto = calcular_pagamento(subtotal, "PIX")

    assert total == 4089
    assert desconto == 611

    # A previa nao altera o pedido.
    assert pedido.total_centavos() == 4700

    return True


def verificar():
    principal = verificar_caso_principal()
    pizza = verificar_pizza()
    bebida = verificar_bebida()
    preservado = verificar_pedido_preservado_em_erro()
    contrato = verificar_item_aceita_qualquer_produto()
    falsa = verificar_previa_falsa()
    transferencia = verificar_transferencia()
    pagamento = verificar_pagamento_regressao()

    return (
        principal and pizza and bebida and preservado
        and contrato and falsa and transferencia and pagamento
    )


if __name__ == "__main__":
    casos = [
        ("Caso principal", verificar_caso_principal),
        ("Pizza", verificar_pizza),
        ("Bebida", verificar_bebida),
        ("Pedido preservado em erro", verificar_pedido_preservado_em_erro),
        ("Item aceita qualquer produto", verificar_item_aceita_qualquer_produto),
        ("Previa falsa", verificar_previa_falsa),
        ("Transferencia", verificar_transferencia),
        ("Pagamento regressao", verificar_pagamento_regressao)
    ]

    todos = True

    for nome, funcao in casos:
        funcao()
        print(f"[OK] {nome}")

    if todos:
        print("Verificacoes concluidas com sucesso.")

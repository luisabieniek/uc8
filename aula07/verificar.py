# Complete os casos do registro; não marque sucesso sem verificá-los.
from modelos import Produto, Item, Pedido

def verificar():
    # TODO: criar dados fictícios, executar e comparar com assert.
    # TODO: testar erro após válido, limites e uma correção com nova execução.
    fruta = Produto("F01", "Fruta", 500)
    leite = Produto("L01", "Leite", 750)

    # Produto
    assert fruta.codigo == "F01"
    assert fruta.nome == "Fruta"
    assert fruta.preco_centavos == 500

    # Item
    item_fruta = Item(fruta, "2")
    assert item_fruta.quantidade == 2
    assert item_fruta.subtotal() == 1000

    # Pedido com duas frutas e três leites
    pedido = Pedido()

    pedido.adicionar(fruta, "2")
    pedido.adicionar(leite, "3")

    # Previsão feita manualmente:
    # 2 × 500 = 1000
    # 3 × 750 = 2250
    # Total = 3250
    assert pedido.total_centavos() == 3250

    # Segundo pedido vazio
    pedido2 = Pedido()

    assert len(pedido2.itens) == 0
    assert pedido2.total_centavos() == 0

    # Repetição por código
    pedido3 = Pedido()

    pedido3.adicionar(fruta, "2")
    pedido3.adicionar(fruta, "2")

    # Seu código soma a quantidade no mesmo item
    assert len(pedido3.itens) == 1
    assert pedido3.itens[0].quantidade == 4
    assert pedido3.total_centavos() == 2000

    # Expectativa deliberadamente errada
    try:
        assert pedido.total_centavos() == 9999
    except AssertionError:
        pass
    else:
        return False

    # Quantidade inválida não altera o pedido válido
    total_antes = pedido.total_centavos()
    itens_antes = len(pedido.itens)

    try:
        pedido.adicionar(fruta, "0")
    except ValueError:
        pass
    else:
        return False

    total_depois = pedido.total_centavos()
    itens_depois = len(pedido.itens)

    assert total_antes == total_depois
    assert itens_antes == itens_depois

    return True

if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")

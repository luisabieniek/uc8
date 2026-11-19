from modelos import Produto
from modelos import Pedido


# Complete os casos do registro; não marque sucesso sem verificá-los.
def verificar():

    # TODO: criar dados fictícios, executar e comparar com assert.

    cafe = Produto("001", "Café", 1500)
    leite = Produto("002", "Leite", 800)

    pedido = Pedido()

    # TODO: testar atualização substituindo quantidade.

    pedido.adicionar(cafe, "2")
    pedido.adicionar(cafe, "3")

    assert pedido.itens["001"].quantidade == 5

    pedido.atualizar("001", "1")

    assert pedido.itens["001"].quantidade == 1

    # TODO: testar total após a atualização.

    pedido.adicionar(leite, "2")

    esperado = (1 * 1500) + (2 * 800)

    assert pedido.total_centavos() == esperado

    # TODO: testar remoção por código.

    pedido.remover("002")

    assert "002" not in pedido.itens

    # TODO: testar erro após válido preservando os dados.

    quantidade_anterior = pedido.itens["001"].quantidade

    try:
        pedido.atualizar("001", "0")
    except ValueError:
        pass

    assert pedido.itens["001"].quantidade == quantidade_anterior

    # TODO: testar limites e nova execução após correção.

    pedido.atualizar("001", "10")

    assert pedido.itens["001"].quantidade == 10

    pedido.atualizar("001", "4")

    assert pedido.itens["001"].quantidade == 4

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
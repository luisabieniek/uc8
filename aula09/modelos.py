# A09: assinaturas de apoio; traga sua implementação anterior.

def quantidade(texto):
    """TODO A09: implemente quantidade conforme o contrato e reutilize seu código anterior."""

    texto = texto.strip()

    if not texto:
        raise ValueError("Quantidade obrigatória.")

    valor = int(texto)

    if valor <= 0:
        raise ValueError("Quantidade deve ser maior que zero.")

    return valor


def formatar(centavos):
    """TODO A09: implemente formatar conforme o contrato e reutilize seu código anterior."""

    return f"R$ {centavos / 100:.2f}".replace(".", ",")


class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        """TODO A09: implemente __init__ conforme o contrato e reutilize seu código anterior."""

        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos


class Item:

    def __init__(self, produto, texto_quantidade):
        """TODO A09: implemente __init__ conforme o contrato e reutilize seu código anterior."""

        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        """TODO A09: implemente subtotal conforme o contrato e reutilize seu código anterior."""

        return self.produto.preco_centavos * self.quantidade


class Pedido:

    def __init__(self):
        """TODO A09: implemente __init__ conforme o contrato e reutilize seu código anterior."""

        self.itens = {}
        self.fechado = False

    def exigir_aberto(self):
        """TODO A09: implemente exigir_aberto conforme o contrato e reutilize seu código anterior."""

        if self.fechado:
            raise ValueError("Pedido fechado.")

    def adicionar(self, produto, texto_quantidade):
        """TODO A09: implemente adicionar conforme o contrato e reutilize seu código anterior."""

        self.exigir_aberto()

        nova_quantidade = quantidade(texto_quantidade)

        if produto.codigo in self.itens:
            self.itens[produto.codigo].quantidade += nova_quantidade
        else:
            self.itens[produto.codigo] = Item(produto, texto_quantidade)

    def total_centavos(self):
        """TODO A09: implemente total_centavos conforme o contrato e reutilize seu código anterior."""

        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        """TODO A09: implemente linhas conforme o contrato e reutilize seu código anterior."""

        linhas = []

        for item in self.itens.values():
            linhas.append(
                {
                    "codigo": item.produto.codigo,
                    "nome": item.produto.nome,
                    "quantidade": item.quantidade,
                    "subtotal": item.subtotal(),
                }
            )

        return linhas

    def atualizar(self, codigo, texto_quantidade):
        """TODO A09: implemente atualizar conforme o contrato e reutilize seu código anterior."""

        self.exigir_aberto()

        if codigo not in self.itens:
            raise ValueError("Código não encontrado.")

        nova_quantidade = quantidade(texto_quantidade)

        # atualizar substitui a quantidade validada
        self.itens[codigo].quantidade = nova_quantidade

    def remover(self, codigo):
        """TODO A09: implemente remover conforme o contrato e reutilize seu código anterior."""

        self.exigir_aberto()

        if codigo not in self.itens:
            raise ValueError("Código não encontrado.")

        # remover apaga a chave do pedido
        del self.itens[codigo]
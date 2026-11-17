# A07: assinaturas de apoio; traga sua implementação anterior.
def quantidade(texto):
    texto = str(texto).strip()

    if not texto.isdigit():
        raise ValueError("Quantidade inválida.")

    valor = int(texto)

    if valor <= 0:
        raise ValueError("Quantidade deve ser maior que zero.")

    return valor

def formatar(centavos):
    """TODO A07: implemente formatar conforme o contrato e reutilize seu código anterior."""
    return f"R$ {centavos / 100:.2f}"

class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        """TODO A07: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos

class Item:

    def __init__(self, produto, texto_quantidade):
        """TODO A07: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        """TODO A07: implemente subtotal conforme o contrato e reutilize seu código anterior."""
        return self.produto.preco_centavos * self.quantidade

class Pedido:

    def __init__(self):
        """TODO A07: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        self.itens = []
        self.aberto = True

    def exigir_aberto(self):
        """TODO A07: implemente exigir_aberto conforme o contrato e reutilize seu código anterior."""
        if not self.aberto:
            raise ValueError("Pedido fechado.")

    def adicionar(self, produto, texto_quantidade):
        """TODO A07: implemente adicionar conforme o contrato e reutilize seu código anterior."""
        self.exigir_aberto()

        qtd = quantidade(texto_quantidade)

        for item in self.itens:
            if item.produto.codigo == produto.codigo:
                item.quantidade += qtd
                return

        self.itens.append(Item(produto, texto_quantidade))

    def total_centavos(self):
        """TODO A07: implemente total_centavos conforme o contrato e reutilize seu código anterior."""
        total = 0

        for item in self.itens:
            total += item.subtotal()

        return total

    def linhas(self):
        """TODO A07: implemente linhas conforme o contrato e reutilize seu código anterior."""
        resultado = []

        for item in self.itens:
            resultado.append(
                f"{item.produto.nome} x{item.quantidade} = "
                f"{formatar(item.subtotal())}"
            )

        return resultado

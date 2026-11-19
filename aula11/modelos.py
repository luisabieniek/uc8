from pagamento import calcular_pagamento


class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        if preco_centavos <= 0:
            raise ValueError("O preço deve ser maior que zero.")

        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos


class Pizza(Produto):
    def __init__(self, codigo, nome, tamanho, preco_centavos):
        super().__init__(codigo, nome, preco_centavos)
        self.tamanho = tamanho


class Bebida(Produto):
    pass


class Item:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade


class Comprovante:
    def __init__(self, itens, pagamento):
        self.itens = [
            {
                "nome": item.produto.nome,
                "quantidade": item.quantidade,
                "preco": item.produto.preco_centavos,
                "subtotal": item.subtotal()
            }
            for item in itens
        ]

        self.pagamento = pagamento


class Pedido:
    def __init__(self):
        self.itens = []
        self.aberto = True
        self._versao = 0

    def versao(self):
        return self._versao

    def adicionar(self, produto, quantidade):
        if not self.aberto:
            raise ValueError("O pedido já foi finalizado.")

        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        for item in self.itens:
            if item.produto.codigo == produto.codigo:
                item.quantidade += quantidade
                self._versao += 1
                return

        self.itens.append(Item(produto, quantidade))
        self._versao += 1

    def atualizar(self, codigo, quantidade):
        if not self.aberto:
            raise ValueError("O pedido já foi finalizado.")

        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        for item in self.itens:
            if item.produto.codigo == codigo:
                item.quantidade = quantidade
                self._versao += 1
                return

        raise ValueError("Item não encontrado.")

    def remover(self, codigo):
        if not self.aberto:
            raise ValueError("O pedido já foi finalizado.")

        for item in self.itens:
            if item.produto.codigo == codigo:
                self.itens.remove(item)
                self._versao += 1
                return

        raise ValueError("Item não encontrado.")

    def calcular_total(self):
        return sum(item.subtotal() for item in self.itens)

    def finalizar(self, forma, versao_previa):
        if not self.aberto:
            raise ValueError("Este pedido já foi finalizado.")

        if not self.itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")

        if versao_previa != self._versao:
            raise ValueError("O pedido foi alterado. Faça uma nova prévia.")

        pagamento = calcular_pagamento(
            self.calcular_total(),
            forma
        )

        comprovante = Comprovante(self.itens, pagamento)
        self.aberto = False

        return comprovante

    def novo(self):
        self.itens = []
        self.aberto = True
        self._versao += 1

"""A12 — classes e regras do pedido."""

from decimal import Decimal
from pagamento import calcular_pagamento


def quantidade(texto):
    try:
        valor = int(str(texto).strip())
    except ValueError:
        raise ValueError("Informe uma quantidade inteira.")

    if valor <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    if valor > 999:
        raise ValueError("A quantidade máxima é 999.")

    return valor


def formatar(centavos):
    reais = centavos // 100
    centavos_restantes = centavos % 100

    return f"R$ {reais},{centavos_restantes:02d}"


class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        codigo = str(codigo).strip()
        nome = str(nome).strip()

        if not codigo or not nome:
            raise ValueError("Código e nome não podem ser vazios.")

        if type(preco_centavos) is not int or preco_centavos <= 0:
            raise ValueError("Preço deve ser inteiro positivo em centavos.")

        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos


class Item:

    def __init__(self, produto, texto_quantidade):
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade


class Comprovante:

    def __init__(self, linhas, total_centavos, forma):
        self.linhas = list(linhas)
        self.total_centavos = total_centavos
        self.forma = forma


class Pedido:

    def __init__(self):
        self.itens = []
        self.aberto = True
        self._versao = 0

    def versao(self):
        return self._versao

    def exigir_aberto(self):
        if not self.aberto:
            raise RuntimeError("O pedido já foi finalizado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()

        qtd = quantidade(texto_quantidade)

        for item in self.itens:
            if item.produto.codigo == produto.codigo:
                if item.quantidade + qtd > 999:
                    raise ValueError("A quantidade máxima é 999.")

                item.quantidade += qtd
                self._versao += 1
                return

        self.itens.append(Item(produto, texto_quantidade))
        self._versao += 1

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()

        nova_quantidade = quantidade(texto_quantidade)

        for item in self.itens:
            if item.produto.codigo == codigo:
                item.quantidade = nova_quantidade
                self._versao += 1
                return

        raise ValueError("Produto não encontrado no pedido.")

    def remover(self, codigo):
        self.exigir_aberto()

        for item in self.itens:
            if item.produto.codigo == codigo:
                self.itens.remove(item)
                self._versao += 1
                return

        raise ValueError("Produto não encontrado no pedido.")

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens)

    def linhas(self):
        resultado = []

        for item in self.itens:
            linha = (
                f"{item.produto.codigo} {item.produto.nome} "
                f"x{item.quantidade} = {formatar(item.subtotal())}"
            )
            resultado.append(linha)

        resultado.append(f"Total: {formatar(self.total_centavos())}")

        return resultado

    def finalizar(self, forma, versao_previa):
        self.exigir_aberto()

        if not self.itens:
            raise ValueError("O pedido está vazio.")

        if versao_previa != self._versao:
            raise ValueError(
                "O pedido foi alterado. Faça uma nova prévia."
            )

        subtotal = str(Decimal(self.total_centavos()) / 100)

        total, desconto = calcular_pagamento(subtotal, forma)

        comprovante = Comprovante(
            self.linhas(),
            total,
            forma
        )

        self.aberto = False

        return comprovante

    def novo(self):
        self.itens = []
        self.aberto = True
        self._versao += 1

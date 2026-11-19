"""A13 — classes do pedido e dos produtos da pizzaria."""

from dataclasses import dataclass
from decimal import Decimal

from pagamento import calcular_pagamento, para_centavos


def formatar(centavos):
    """Formata um valor inteiro em centavos como moeda brasileira."""
    centavos = int(centavos)
    sinal = "-" if centavos < 0 else ""
    centavos = abs(centavos)
    reais = centavos // 100
    parte_centavos = centavos % 100
    return f"{sinal}R$ {reais:,}".replace(",", ".") + f",{parte_centavos:02d}"


@dataclass(frozen=True)
class Produto:
    codigo: str
    nome: str
    preco_centavos: int

    def __post_init__(self):
        codigo = str(self.codigo).strip()
        nome = str(self.nome).strip()

        if not codigo:
            raise ValueError("O código do produto não pode ficar vazio.")
        if not nome:
            raise ValueError("O nome do produto não pode ficar vazio.")
        if isinstance(self.preco_centavos, bool) or not isinstance(
            self.preco_centavos, int
        ):
            raise ValueError("O preço deve ser informado em centavos inteiros.")
        if self.preco_centavos <= 0:
            raise ValueError("O preço deve ser maior que zero.")

        object.__setattr__(self, "codigo", codigo)
        object.__setattr__(self, "nome", nome)


@dataclass
class Item:
    produto: Produto
    quantidade: int

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade


@dataclass(frozen=True)
class Comprovante:
    linhas: tuple
    forma: str
    subtotal_centavos: int
    desconto_centavos: int
    total_centavos: int


class Pedido:
    def __init__(self):
        self.itens = []
        self._versao = 0
        self._finalizado = False

    def _verificar_aberto(self):
        if self._finalizado:
            raise RuntimeError("Este pedido já foi confirmado. Inicie um novo pedido.")

    @staticmethod
    def _ler_quantidade(valor):
        texto = str(valor).strip()
        if not texto.isdigit():
            raise ValueError("A quantidade deve ser um número inteiro positivo.")

        quantidade = int(texto)
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return quantidade

    def adicionar(self, produto, quantidade):
        self._verificar_aberto()

        if not isinstance(produto, Produto):
            raise ValueError("Selecione um produto válido.")

        qtd = self._ler_quantidade(quantidade)

        for item in self.itens:
            if item.produto.codigo == produto.codigo:
                item.quantidade += qtd
                self._versao += 1
                return

        self.itens.append(Item(produto, qtd))
        self._versao += 1

    def atualizar(self, codigo, quantidade):
        self._verificar_aberto()
        qtd = self._ler_quantidade(quantidade)

        for item in self.itens:
            if item.produto.codigo == str(codigo):
                item.quantidade = qtd
                self._versao += 1
                return

        raise ValueError("O produto selecionado não está no pedido.")

    def remover(self, codigo):
        self._verificar_aberto()

        for indice, item in enumerate(self.itens):
            if item.produto.codigo == str(codigo):
                del self.itens[indice]
                self._versao += 1
                return

        raise ValueError("O produto selecionado não está no pedido.")

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens)

    def linhas(self):
        return [
            f"{item.produto.nome} x{item.quantidade} — "
            f"{formatar(item.subtotal())}"
            for item in self.itens
        ]

    def versao(self):
        return self._versao

    def finalizar(self, forma, versao_esperada=None):
        self._verificar_aberto()

        if not self.itens:
            raise ValueError("Não é possível confirmar um pedido vazio.")

        if versao_esperada is not None and versao_esperada != self._versao:
            raise RuntimeError(
                "O pedido foi alterado depois da prévia. Gere a prévia novamente."
            )

        subtotal = self.total_centavos()
        valor = f"{Decimal(subtotal) / Decimal(100):.2f}"
        total, desconto = calcular_pagamento(valor, forma)

        comprovante = Comprovante(
            linhas=tuple(self.linhas()),
            forma=forma,
            subtotal_centavos=subtotal,
            desconto_centavos=desconto,
            total_centavos=total,
        )
        self._finalizado = True
        self._versao += 1
        return comprovante

    def novo(self):
        self.itens.clear()
        self._finalizado = False
        self._versao += 1

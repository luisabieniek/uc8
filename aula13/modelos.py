from pagamento import calcular_pagamento

TAMANHOS = ("Media", "Grande")


def formatar(centavos):
    sinal = "-" if centavos < 0 else ""
    reais, resto = divmod(abs(centavos), 100)
    return f"R$ {sinal}{reais},{resto:02d}"


class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        codigo = codigo.strip()
        nome = nome.strip()
        if not codigo or not nome:
            raise ValueError("Informe código e nome.")
        if type(preco_centavos) is not int or preco_centavos <= 0:
            raise ValueError("O preço deve ser um inteiro positivo em centavos.")
        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos


class Pizza(Produto):
    def __init__(self, codigo, nome, tamanho, preco_centavos):
        if tamanho not in TAMANHOS:
            raise ValueError("Tamanho inválido.")
        super().__init__(codigo, nome, preco_centavos)
        self.tamanho = tamanho


class Bebida(Produto):
    pass


def validar_quantidade(texto):
    texto = texto.strip()
    if not texto.isascii() or not texto.isdecimal():
        raise ValueError("Informe uma quantidade inteira positiva.")
    quantidade = int(texto)
    if quantidade <= 0:
        raise ValueError("Informe uma quantidade inteira positiva.")
    return quantidade


class Item:
    def __init__(self, produto, texto_quantidade):
        self.produto = produto
        self.quantidade = validar_quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade


class Comprovante:
    def __init__(self, linhas, total_centavos, forma):
        self.linhas = linhas.copy()
        self.total_centavos = total_centavos
        self.forma = forma
        subtotal = f"{total_centavos // 100}.{total_centavos % 100:02d}"
        self.total_pago_centavos, self.desconto_centavos = calcular_pagamento(subtotal, forma)


class Pedido:
    def __init__(self):
        self._contador = 0
        self.novo()

    def novo(self):
        self.itens = []
        self.aberto = True
        self._versao = 0

    def versao(self):
        return self._versao

    def _registrar_alteracao(self):
        self._contador += 1
        self._versao = self._contador

    def _conferir_aberto(self):
        if not self.aberto:
            raise RuntimeError("Pedido já finalizado.")

    def _buscar(self, codigo):
        for item in self.itens:
            if item.produto.codigo == codigo:
                return item
        return None

    def adicionar(self, produto, texto_quantidade):
        self._conferir_aberto()
        novo_item = Item(produto, texto_quantidade)
        item = self._buscar(produto.codigo)
        if item is None:
            self.itens.append(novo_item)
        else:
            item.quantidade += novo_item.quantidade
        self._registrar_alteracao()

    def atualizar(self, codigo, texto_quantidade):
        self._conferir_aberto()
        item = self._buscar(codigo)
        if item is None:
            raise ValueError("O produto nao esta no pedido.")
        item.quantidade = validar_quantidade(texto_quantidade)
        self._registrar_alteracao()

    def remover(self, codigo):
        self._conferir_aberto()
        item = self._buscar(codigo)
        if item is None:
            raise ValueError("O produto nao esta no pedido.")
        self.itens.remove(item)
        self._registrar_alteracao()

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens)

    def linhas(self):
        linhas = []
        for item in self.itens:
            produto = item.produto
            nome = produto.nome
            if isinstance(produto, Pizza):
                nome = f"{nome} ({produto.tamanho})"
            linhas.append(f"{item.quantidade} x {nome} — {formatar(item.subtotal())}")
        return linhas

    def finalizar(self, forma, versao_previa):
        self._conferir_aberto()
        if not self.itens:
            raise ValueError("Pedido vazio.")
        if versao_previa != self.versao():
            raise ValueError("O pedido foi alterado. Abra uma nova prévia.")
        comprovante = Comprovante(self.linhas(), self.total_centavos(), forma)
        self.aberto = False
        return comprovante

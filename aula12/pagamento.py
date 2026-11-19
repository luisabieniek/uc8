
"""A12 — validação e cálculo de pagamentos."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


FATORES = {
    "Dinheiro": "0.87",
    "PIX": "0.87",
    "Débito": "0.92",
    "Crédito 1x": "1.00"
}


def valor_monetario(texto, permitir_zero=True):
    texto = str(texto).strip().replace(",", ".")

    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("Valor monetário inválido.")

    if not valor.is_finite():
        raise ValueError("Valor monetário inválido.")

    if valor < 0:
        raise ValueError("O valor não pode ser negativo.")

    if not permitir_zero and valor == 0:
        raise ValueError("O valor não pode ser zero.")

    return valor


def calcular_pagamento(subtotal_texto, forma):
    if forma not in FATORES:
        raise ValueError("Forma de pagamento desconhecida.")

    subtotal = valor_monetario(subtotal_texto)

    subtotal_centavos = (
        subtotal * 100
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    fator = Decimal(FATORES[forma])

    total = (
        subtotal_centavos * fator
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    desconto = subtotal_centavos - total

    return int(total), int(desconto)


def preco_para_centavos(texto):
    valor = valor_monetario(texto, permitir_zero=False)

    centavos = (
        valor * 100
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    return int(centavos)

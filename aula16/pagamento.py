"""A12 — interpretação monetária e cálculo de pagamento."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}


def valor_monetario(texto, permitir_zero=True):
    texto = str(texto).strip().replace(',', '.')
    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError(f"Valor monetário inválido: '{texto}'.")
    if not valor.is_finite() or valor < 0:
        raise ValueError('Informe um valor válido e não negativo.')
    if not permitir_zero and valor == 0:
        raise ValueError('Valor não pode ser zero.')
    return valor


def calcular_pagamento(subtotal_texto, forma):
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento desconhecida: '{forma}'.")
    valor = valor_monetario(subtotal_texto)
    centavos = (valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    total = (centavos * Decimal(FATORES[forma])).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return int(total), int(centavos - total)


def preco_para_centavos(texto):
    valor = valor_monetario(texto, permitir_zero=False)
    return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

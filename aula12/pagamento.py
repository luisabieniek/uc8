import re
from decimal import Decimal, ROUND_HALF_UP


FATORES = {
    "Dinheiro": "0.87",
    "PIX": "0.87",
    "Débito": "0.92",
    "Crédito 1x": "1.00",
}


def valor_monetario(texto):
    texto = texto.strip()
    if re.fullmatch(r"[0-9]+(?:[.,][0-9]{1,2})?", texto) is None:
        raise ValueError("Informe um valor com até duas casas decimais.")
    return Decimal(texto.replace(",", "."))


def calcular_pagamento(subtotal_texto, forma):
    if forma not in FATORES:
        raise ValueError("Selecione uma forma de pagamento válida.")
    centavos = int(valor_monetario(subtotal_texto) * 100)
    fator = Decimal(FATORES[forma])
    total = int((centavos * fator).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return total, centavos - total

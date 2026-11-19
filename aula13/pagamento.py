"""A13 — cálculo monetário com Decimal e valores inteiros em centavos."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


# Fator aplicado ao subtotal conforme a forma de pagamento.
# 0.95 representa 5% de desconto; 1.00 mantém o valor original.
FATORES = {
    "Dinheiro": Decimal("0.95"),
    "Pix": Decimal("0.95"),
    "Débito": Decimal("1.00"),
    "Crédito": Decimal("1.00"),
}


def para_decimal(valor):
    texto = str(valor).strip().replace(",", ".")
    if not texto:
        raise ValueError("Informe um valor para o pagamento.")

    try:
        numero = Decimal(texto)
    except (InvalidOperation, ValueError):
        raise ValueError("O valor informado não é válido.") from None

    if not numero.is_finite() or numero <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    return numero


def para_centavos(valor):
    numero = para_decimal(valor)
    return int(
        (numero * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )


def calcular_pagamento(valor, forma):
    """Retorna (total_final_em_centavos, desconto_em_centavos)."""
    if forma not in FATORES:
        raise ValueError("Selecione uma forma de pagamento válida.")

    subtotal = para_decimal(valor)
    fator = FATORES[forma]

    total_decimal = (subtotal * fator).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    subtotal_centavos = int(
        (subtotal * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )
    total_centavos = int(total_decimal * 100)
    desconto_centavos = subtotal_centavos - total_centavos

    return total_centavos, desconto_centavos

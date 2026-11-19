from decimal import Decimal, ROUND_HALF_UP


FATORES = {
    "Dinheiro": Decimal("0.87"),
    "PIX": Decimal("0.87"),
    "Débito": Decimal("0.92"),
    "Crédito": Decimal("1.00")
}


def calcular_pagamento(total_centavos, forma):
    if forma not in FATORES:
        raise ValueError("Forma de pagamento inválida.")

    total = Decimal(total_centavos) / Decimal("100")
    valor_final = total * FATORES[forma]

    valor_final = valor_final.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return {
        "forma": forma,
        "total": total,
        "valor_final": valor_final
    }


def formatar_dinheiro(valor):
    valor = Decimal(valor).quantize(Decimal("0.01"))

    return f"R$ {valor:.2f}".replace(".", ",")
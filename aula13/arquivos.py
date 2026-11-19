"""A13 — leitura, validação e gravação segura do catálogo JSON."""

import json
import os
import tempfile
from pathlib import Path


def validar_catalogo(dados):
    if not isinstance(dados, list):
        raise ValueError("O catálogo precisa ser uma lista JSON.")

    codigos = set()

    for indice, item in enumerate(dados, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"O produto {indice} precisa ser um objeto JSON.")

        if set(item) != {"id", "nome", "preco_centavos"}:
            raise ValueError(
                f"O produto {indice} deve conter id, nome e preco_centavos."
            )

        codigo = str(item["id"]).strip()
        nome = str(item["nome"]).strip()
        preco = item["preco_centavos"]

        if not codigo:
            raise ValueError(f"O produto {indice} está sem id.")
        if codigo in codigos:
            raise ValueError(f"ID de produto duplicado: {codigo}.")
        if not nome:
            raise ValueError(f"O produto {codigo} está sem nome.")
        if isinstance(preco, bool) or not isinstance(preco, int) or preco <= 0:
            raise ValueError(
                f"O preço do produto {codigo} deve ser inteiro e maior que zero."
            )

        codigos.add(codigo)

    return True


def ler_catalogo(caminho):
    caminho = Path(caminho)

    if not caminho.exists():
        return None

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    validar_catalogo(dados)
    return dados


def salvar_catalogo(caminho, dados):
    caminho = Path(caminho)
    validar_catalogo(dados)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            dir=caminho.parent,
            prefix=f".{caminho.name}.",
            suffix=".tmp",
            delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())

        os.replace(temporario, caminho)
    except Exception:
        if temporario is not None and temporario.exists():
            temporario.unlink()
        raise

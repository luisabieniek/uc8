
"""A12 — leitura, validação e gravação do catálogo JSON."""

import json
import os
import tempfile
from pathlib import Path

from modelos import Produto


def validar_catalogo(dados):
    if not isinstance(dados, list):
        raise ValueError("Catálogo deve ser uma lista.")

    ids_vistos = set()

    for indice, item in enumerate(dados):
        if not isinstance(item, dict):
            raise ValueError(f"Item {indice} deve ser um objeto.")

        for campo in ("id", "nome", "preco_centavos"):
            if campo not in item:
                raise ValueError(
                    f"Item {indice} sem o campo '{campo}'."
                )

        codigo = item["id"]
        nome = item["nome"]
        preco = item["preco_centavos"]

        if type(codigo) not in (str, int):
            raise ValueError(
                f"Item {indice}: ID deve ser texto ou inteiro."
            )

        if not isinstance(nome, str) or not nome.strip():
            raise ValueError(
                f"Item {indice}: nome não pode ser vazio."
            )

        if type(preco) is not int or preco <= 0:
            raise ValueError(
                f"Item {indice}: preço deve ser inteiro positivo."
            )

        codigo_texto = str(codigo).strip()

        if not codigo_texto:
            raise ValueError(f"Item {indice}: ID não pode ser vazio.")

        if codigo_texto in ids_vistos:
            raise ValueError(f"ID repetido: {codigo_texto}.")

        ids_vistos.add(codigo_texto)

    return dados


def ler_catalogo(caminho):
    caminho = Path(caminho)

    if not caminho.exists():
        return None

    try:
        texto = caminho.read_text(encoding="utf-8")
        dados = json.loads(texto)

    except (UnicodeDecodeError, json.JSONDecodeError) as erro:
        raise ValueError(
            f"JSON inválido em '{caminho}': {erro}"
        ) from erro

    return validar_catalogo(dados)


def carregar_catalogo(caminho):
    dados = ler_catalogo(caminho)

    if dados is None:
        return False, "Arquivo não encontrado", []

    produtos = []

    for item in dados:
        produto = Produto(
            item["id"],
            item["nome"],
            item["preco_centavos"]
        )
        produtos.append(produto)

    return True, "Catálogo carregado", produtos


def salvar_catalogo(caminho, dados):
    caminho = Path(caminho)

    validar_catalogo(dados)

    texto = json.dumps(
        dados,
        ensure_ascii=False,
        indent=4
    )

    if not caminho.parent.exists():
        raise FileNotFoundError(
            "A pasta de destino não existe."
        )

    arquivo_temporario = None

    try:
        descritor, arquivo_temporario = tempfile.mkstemp(
            dir=caminho.parent,
            suffix=".tmp"
        )

        with os.fdopen(
            descritor,
            "w",
            encoding="utf-8"
        ) as arquivo:
            arquivo.write(texto)

        os.replace(arquivo_temporario, caminho)

    except Exception:
        if arquivo_temporario and os.path.exists(arquivo_temporario):
            os.unlink(arquivo_temporario)

        raise

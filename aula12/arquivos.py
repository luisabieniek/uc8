import json
import os
import tempfile
from pathlib import Path
from modelos import Produto


def validar_catalogo(dados):
    if not isinstance(dados, list):
        raise ValueError("O catálogo deve ser uma lista de produtos.")

    codigos = set()
    for numero, item in enumerate(dados, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Produto {numero}: informe um objeto JSON.")

        codigo = item.get("id")
        nome = item.get("nome")
        preco = item.get("preco_centavos")
        if not isinstance(codigo, str) or not isinstance(nome, str):
            raise ValueError(f"Produto {numero}: id e nome devem ser textos.")

        produto = Produto(codigo, nome, preco)
        if produto.codigo in codigos:
            raise ValueError(f"Código repetido: {produto.codigo}.")
        codigos.add(produto.codigo)


def ler_catalogo(caminho):
    try:
        with Path(caminho).open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        return None
    validar_catalogo(dados)
    return dados


def salvar_catalogo(caminho, dados):
    validar_catalogo(dados)
    caminho = Path(caminho)
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=caminho.parent, delete=False
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            arquivo.write("\n")
        os.replace(temporario, caminho)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)

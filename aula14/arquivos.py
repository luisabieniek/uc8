"""A12 — leitura e gravação segura do catálogo JSON."""
import json
import os
import tempfile
from pathlib import Path
from modelos import Produto


def carregar_catalogo(caminho):
    dados = ler_catalogo(caminho)
    if dados is None:
        return False, 'Arquivo não encontrado', []
    produtos = []
    for item in dados:
        produtos.append(Produto(item['id'], item['nome'], item['preco_centavos']))
    return True, 'Catálogo carregado', produtos


def validar_catalogo(dados):
    if not isinstance(dados, list):
        raise ValueError('Catálogo deve ser uma lista.')
    ids = set()
    for i, item in enumerate(dados):
        if not isinstance(item, dict):
            raise ValueError(f'Item {i} deve ser um objeto.')
        for campo in ('id', 'nome', 'preco_centavos'):
            if campo not in item:
                raise ValueError(f"Item {i} sem campo '{campo}'.")
        if type(item['id']) not in (str, int):
            raise ValueError('ID inválido.')
        if type(item['preco_centavos']) is not int or item['preco_centavos'] <= 0:
            raise ValueError('Preço inválido.')
        if not isinstance(item['nome'], str) or not item['nome'].strip():
            raise ValueError('Nome inválido.')
        codigo = str(item['id']).strip()
        if not codigo or codigo in ids:
            raise ValueError('ID vazio ou repetido.')
        ids.add(codigo)
    return dados


def ler_catalogo(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return None
    try:
        dados = json.loads(caminho.read_text(encoding='utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError) as erro:
        raise ValueError(f'JSON inválido: {erro}') from erro
    return validar_catalogo(dados)


def salvar_catalogo(caminho, dados):
    validar_catalogo(dados)
    caminho = Path(caminho)
    texto = json.dumps(dados, ensure_ascii=False, indent=4)
    fd, temporario = tempfile.mkstemp(dir=caminho.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as arquivo:
            arquivo.write(texto)
        os.replace(temporario, caminho)
    except Exception:
        if os.path.exists(temporario):
            os.unlink(temporario)
        raise

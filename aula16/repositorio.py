# A14: assinaturas de apoio; traga sua implementação anterior.
from contextlib import closing
from pathlib import Path
import sqlite3

from banco import (
    CAMINHO_BANCO, criar_banco,
    listar_produtos as buscar_produtos,
    salvar_produto as inserir_produto,
    atualizar_produto as editar_produto,
    remover_produto as excluir_produto,
)


def validar_nome(nome):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("Informe um nome válido.")
    return nome.strip()


def validar_id(codigo):
    if isinstance(codigo, bool) or not isinstance(codigo, (str, int)) or not str(codigo).strip():
        raise ValueError("Informe um código válido.")
    return str(codigo).strip()


def validar_preco(preco):
    if type(preco) is not int or preco <= 0:
        raise ValueError("O preço deve ser um inteiro positivo em centavos.")
    return preco


class RepositorioProdutos:
    """Contrato para repositórios de produtos, independente do armazenamento."""

    def listar(self):
        raise NotImplementedError

    def salvar(self, codigo, nome, preco):
        raise NotImplementedError

    def atualizar(self, codigo, nome, preco):
        raise NotImplementedError

    def remover(self, codigo):
        raise NotImplementedError


class ProdutosSQLite(RepositorioProdutos):
    """Adapter do contrato de produtos para o banco SQLite."""

    def __init__(self, caminho=CAMINHO_BANCO):
        self.caminho = Path(caminho)

    def iniciar(self):
        criar_banco(self.caminho, self.caminho.with_name("catalogo.json"))

    def listar(self):
        return buscar_produtos(self.caminho)

    def salvar(self, codigo, nome, preco):
        return inserir_produto(validar_id(codigo), validar_nome(nome), validar_preco(preco), self.caminho)

    def atualizar(self, codigo, nome, preco):
        return editar_produto(validar_id(codigo), validar_nome(nome), validar_preco(preco), self.caminho)

    def remover(self, codigo):
        return excluir_produto(validar_id(codigo), self.caminho)


class RepositorioSqlite:
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def conectar(self):
        return sqlite3.connect(self.caminho)

    def iniciar(self):
        criar_banco(self.caminho, self.caminho.with_name("catalogo.json"))

    def adicionar_produto(self, nome, preco):
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        with closing(self.conectar()) as conexao:
            with conexao:
                codigos = conexao.execute("SELECT codigo FROM produtos").fetchall()
                numeros = [int(codigo) for (codigo,) in codigos if codigo.isdigit()]
                codigo = str(max(numeros, default=0) + 1)
                conexao.execute(
                    "INSERT INTO produtos (codigo, nome, preco_centavos) VALUES (?, ?, ?)",
                    (codigo, nome, preco),
                )
                return int(codigo)

    def listar_produtos(self):
        return buscar_produtos(self.caminho)

    def editar_produto(self, codigo, nome, preco):
        return editar_produto(validar_id(codigo), validar_nome(nome), validar_preco(preco), self.caminho)

    def excluir_produto(self, codigo, confirmado=False):
        if not confirmado:
            return False
        return excluir_produto(validar_id(codigo), self.caminho)

    def adicionar_cliente(self, nome):
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("INSERT INTO clientes (nome) VALUES (?)", (validar_nome(nome),))
                return cursor.lastrowid

    def listar_clientes(self):
        with closing(self.conectar()) as conexao:
            return conexao.execute("SELECT id, nome, telefone FROM clientes ORDER BY nome, id").fetchall()

    def editar_cliente(self, codigo, nome):
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("UPDATE clientes SET nome = ? WHERE id = ?", (validar_nome(nome), int(validar_id(codigo))))
                return cursor.rowcount > 0

    def excluir_cliente(self, codigo, confirmado=False):
        if not confirmado:
            return False
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("DELETE FROM clientes WHERE id = ?", (int(validar_id(codigo)),))
                return cursor.rowcount > 0

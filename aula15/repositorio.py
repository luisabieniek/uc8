from contextlib import closing
from pathlib import Path
import sqlite3

from banco import criar_banco


def validar_nome(nome):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("Informe um nome válido.")
    return nome.strip()


def validar_id(codigo):
    if type(codigo) is not int or codigo <= 0:
        raise ValueError("O ID deve ser um inteiro positivo.")
    return codigo


def validar_preco(preco):
    if type(preco) is not int or preco <= 0:
        raise ValueError("O preço deve ser um inteiro positivo em centavos.")
    return preco


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
                    (codigo, nome, preco)
                )
                return int(codigo)

    def listar_produtos(self):
        with closing(self.conectar()) as conexao:
            return conexao.execute(
                "SELECT codigo, nome, preco_centavos FROM produtos ORDER BY codigo"
            ).fetchall()

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    "INSERT INTO clientes (nome) VALUES (?)", (nome,)
                )
                return cursor.lastrowid

    def listar_clientes(self):
        with closing(self.conectar()) as conexao:
            return conexao.execute(
                "SELECT id, nome, telefone FROM clientes ORDER BY nome, id"
            ).fetchall()

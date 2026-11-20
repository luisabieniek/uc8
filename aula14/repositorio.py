from contextlib import closing
from pathlib import Path
import sqlite3


def validar_nome(nome):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError('Informe um nome válido.')
    return nome.strip()


def validar_id(codigo):
    if type(codigo) is not int or codigo <= 0:
        raise ValueError('O ID deve ser um inteiro positivo.')
    return codigo


def validar_preco(preco):
    if type(preco) is not int or preco <= 0:
        raise ValueError('O preço deve ser um inteiro positivo em centavos.')
    return preco


class RepositorioSqlite:
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.execute('PRAGMA foreign_keys = ON')
        return conexao

    def iniciar(self):
        with closing(self.conectar()) as conexao:
            with conexao:
                conexao.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco_centavos INTEGER NOT NULL CHECK (preco_centavos > 0)
                )''')
                conexao.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                )''')

    def adicionar_produto(self, nome, preco):
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    'INSERT INTO produtos (nome, preco_centavos) VALUES (?, ?)',
                    (nome, preco)
                )
                return cursor.lastrowid

    def listar_produtos(self):
        with closing(self.conectar()) as conexao:
            return conexao.execute(
                'SELECT id, nome, preco_centavos FROM produtos ORDER BY id'
            ).fetchall()

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    'INSERT INTO clientes (nome) VALUES (?)', (nome,)
                )
                return cursor.lastrowid

    def listar_clientes(self):
        with closing(self.conectar()) as conexao:
            return conexao.execute('SELECT id, nome FROM clientes ORDER BY id').fetchall()

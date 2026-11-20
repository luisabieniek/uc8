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
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("DELETE FROM produtos WHERE codigo = ?", (validar_id(codigo),))
                return cursor.rowcount > 0


class RepositorioSqlite:
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

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
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("DELETE FROM produtos WHERE codigo = ?", (validar_id(codigo),))
                return cursor.rowcount > 0

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

    def iniciar_vendas(self):
        with closing(self.conectar()) as conexao:
            with conexao:
                conexao.execute("""CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
                    forma TEXT NOT NULL, total_centavos INTEGER NOT NULL)""")
                conexao.execute("""CREATE TABLE IF NOT EXISTS itens_venda (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER NOT NULL REFERENCES vendas(id) ON DELETE RESTRICT,
                    produto_codigo TEXT NOT NULL REFERENCES produtos(codigo) ON DELETE RESTRICT,
                    quantidade INTEGER NOT NULL, preco_centavos INTEGER NOT NULL)""")

    def registrar_venda(self, cliente_id, itens, forma):
        from pagamento import calcular_pagamento
        if type(cliente_id) is not int or cliente_id <= 0:
            raise ValueError("Selecione um cliente válido.")
        if not itens:
            raise ValueError("Adicione produtos ao pedido.")
        self.iniciar_vendas()
        with closing(self.conectar()) as conexao:
            with conexao:
                if not conexao.execute("SELECT 1 FROM clientes WHERE id = ?", (cliente_id,)).fetchone():
                    raise ValueError("Cliente não encontrado.")
                subtotal = 0
                linhas = []
                for item in itens:
                    if hasattr(item, "produto"):
                        codigo, qtd = item.produto.codigo, item.quantidade
                    else:
                        codigo, qtd = item[0], item[1]
                    if type(qtd) is not int or qtd <= 0 or qtd > 999:
                        raise ValueError("Quantidade inválida.")
                    produto = conexao.execute("SELECT preco_centavos FROM produtos WHERE codigo = ?", (str(codigo),)).fetchone()
                    if produto is None:
                        raise ValueError("Produto não encontrado no catálogo.")
                    preco = produto[0]
                    if hasattr(item, "produto") and item.produto.preco_centavos != preco:
                        raise ValueError("Preço alterado. Atualize o pedido antes de confirmar.")
                    subtotal += preco * qtd
                    linhas.append((str(codigo), qtd, preco))
                total, desconto = calcular_pagamento(str(subtotal / 100), forma)
                cursor = conexao.execute("INSERT INTO vendas (cliente_id, forma, total_centavos) VALUES (?, ?, ?)", (cliente_id, forma, total))
                venda_id = cursor.lastrowid
                for codigo, qtd, preco in linhas:
                    conexao.execute("INSERT INTO itens_venda (venda_id, produto_codigo, quantidade, preco_centavos) VALUES (?, ?, ?, ?)", (venda_id, codigo, qtd, preco))
                return venda_id, total

    def listar_vendas(self):
        self.iniciar_vendas()
        with closing(self.conectar()) as conexao:
            return conexao.execute("SELECT id, cliente_id, forma, total_centavos FROM vendas ORDER BY id").fetchall()

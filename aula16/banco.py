"""Acesso ao banco SQLite de produtos da aula 14."""
import sqlite3
from contextlib import closing
from pathlib import Path
from arquivos import ler_catalogo, validar_catalogo

CAMINHO_BANCO = Path(__file__).with_name('produtos.db')
CAMINHO_CATALOGO = Path(__file__).with_name('catalogo.json')


def _conectar(caminho):
    return sqlite3.connect(caminho)


def _validar_codigo(codigo):
    if not isinstance(codigo, str) or not codigo.strip():
        raise ValueError('Informe o código do produto.')
    return codigo.strip()


def _validar_nome(nome):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError('Informe o nome do produto.')
    return nome.strip()


def _validar_preco(preco_centavos):
    if type(preco_centavos) is not int or preco_centavos <= 0:
        raise ValueError('Informe um preço positivo em centavos.')
    return preco_centavos


def _salvar_produto(conexao, codigo, nome, preco_centavos):
    conexao.execute('INSERT INTO produtos (codigo, nome, preco_centavos) VALUES (?, ?, ?)',
                    (_validar_codigo(codigo), _validar_nome(nome), _validar_preco(preco_centavos)))


def _atualizar_produto(conexao, codigo, nome, preco_centavos):
    cursor = conexao.execute('UPDATE produtos SET nome = ?, preco_centavos = ? WHERE codigo = ?',
                             (_validar_nome(nome), _validar_preco(preco_centavos), _validar_codigo(codigo)))
    return cursor.rowcount > 0


def _remover_produto(conexao, codigo):
    cursor = conexao.execute('DELETE FROM produtos WHERE codigo = ?', (_validar_codigo(codigo),))
    return cursor.rowcount > 0


def _importar_catalogo_json(conexao, caminho_catalogo):
    dados = ler_catalogo(caminho_catalogo)
    if dados is None:
        return 0
    for produto in dados:
        _salvar_produto(conexao, str(produto['id']), produto['nome'], produto['preco_centavos'])
    return len(dados)


def criar_banco(caminho=CAMINHO_BANCO, caminho_catalogo=CAMINHO_CATALOGO):
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            conexao.execute('''CREATE TABLE IF NOT EXISTS produtos (
                codigo TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                preco_centavos INTEGER NOT NULL CHECK (preco_centavos > 0)
            )''')
            conexao.execute("""CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT
            )""")
            total = conexao.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
            if total == 0:
                _importar_catalogo_json(conexao, caminho_catalogo)


def listar_produtos(caminho=CAMINHO_BANCO):
    with closing(_conectar(caminho)) as conexao:
        return conexao.execute('SELECT codigo, nome, preco_centavos FROM produtos ORDER BY codigo').fetchall()


def salvar_produto(codigo, nome, preco_centavos, caminho=CAMINHO_BANCO):
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            _salvar_produto(conexao, codigo, nome, preco_centavos)


def atualizar_produto(codigo, nome, preco_centavos, caminho=CAMINHO_BANCO):
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            return _atualizar_produto(conexao, codigo, nome, preco_centavos)


def remover_produto(codigo, caminho=CAMINHO_BANCO):
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            return _remover_produto(conexao, codigo)


def sincronizar_produtos(produtos, caminho=CAMINHO_BANCO):
    validar_catalogo(produtos)
    desejados = {}
    for produto in produtos:
        codigo = _validar_codigo(str(produto['id']))
        desejados[codigo] = (_validar_nome(produto['nome']), _validar_preco(produto['preco_centavos']))

    resultado = {'inseridos': 0, 'atualizados': 0, 'removidos': 0}
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            atuais = {}
            for codigo, nome, preco in conexao.execute('SELECT codigo, nome, preco_centavos FROM produtos'):
                atuais[codigo] = (nome, preco)

            for codigo, dados in desejados.items():
                nome, preco = dados
                if codigo not in atuais:
                    _salvar_produto(conexao, codigo, nome, preco)
                    resultado['inseridos'] += 1
                elif atuais[codigo] != dados:
                    _atualizar_produto(conexao, codigo, nome, preco)
                    resultado['atualizados'] += 1

            for codigo in atuais:
                if codigo not in desejados:
                    _remover_produto(conexao, codigo)
                    resultado['removidos'] += 1
    return resultado


def _validar_id_cliente(cliente_id):
    if type(cliente_id) is not int or cliente_id <= 0:
        raise ValueError("O ID do cliente deve ser um inteiro positivo.")
    return cliente_id


def _validar_telefone(telefone):
    if telefone is None:
        return None
    if not isinstance(telefone, str):
        raise ValueError("O telefone deve ser informado como texto.")
    return telefone.strip() or None


def listar_clientes(caminho=CAMINHO_BANCO):
    with closing(_conectar(caminho)) as conexao:
        return conexao.execute(
            "SELECT id, nome, telefone FROM clientes ORDER BY nome, id"
        ).fetchall()


def salvar_cliente(nome, telefone=None, caminho=CAMINHO_BANCO):
    nome = _validar_nome(nome)
    telefone = _validar_telefone(telefone)
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            cursor = conexao.execute(
                "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
                (nome, telefone)
            )
            return cursor.lastrowid


def atualizar_cliente(cliente_id, nome, telefone=None, caminho=CAMINHO_BANCO):
    cliente_id = _validar_id_cliente(cliente_id)
    nome = _validar_nome(nome)
    telefone = _validar_telefone(telefone)
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            cursor = conexao.execute(
                "UPDATE clientes SET nome = ?, telefone = ? WHERE id = ?",
                (nome, telefone, cliente_id)
            )
            return cursor.rowcount > 0


def remover_cliente(cliente_id, caminho=CAMINHO_BANCO):
    cliente_id = _validar_id_cliente(cliente_id)
    with closing(_conectar(caminho)) as conexao:
        with conexao:
            cursor = conexao.execute(
                "DELETE FROM clientes WHERE id = ?", (cliente_id,)
            )
            return cursor.rowcount > 0

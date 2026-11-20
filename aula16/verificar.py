"""Testes sem interface para CSV, sessões de perfil e SQLite."""
import csv
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from banco import criar_banco, salvar_produto, atualizar_produto, remover_produto, listar_produtos, sincronizar_produtos, salvar_cliente, listar_clientes, atualizar_cliente, remover_cliente
from modelos import Comprovante, Pedido, Produto
from perfis import SessaoDemo
from relatorios import exportar_csv, registrar_venda_csv
from repositorio import RepositorioSqlite, ProdutosSQLite
from memoria import RepositorioMemoria, ProdutosMemoria
from controller import CadastroController, ProdutoController


def verificar_sqlite():
    with TemporaryDirectory() as pasta:
        banco = Path(pasta) / 'produtos.db'
        criar_banco(banco, Path(pasta) / 'ausente.json')
        salvar_produto('P99', 'Pizza Especial', 5990, banco)
        assert listar_produtos(banco) == [('P99', 'Pizza Especial', 5990)]
        assert atualizar_produto('P99', 'Pizza Especial', 6490, banco)
        assert listar_produtos(banco)[0][2] == 6490
        assert remover_produto('P99', banco)
        assert listar_produtos(banco) == []
        resultado = sincronizar_produtos([{'id': 1, 'nome': 'Arroz', 'preco_centavos': 2590}], banco)
        assert resultado['inseridos'] == 1


def verificar_clientes():
    with TemporaryDirectory() as pasta:
        banco = Path(pasta) / 'clientes.db'
        criar_banco(banco, Path(pasta) / 'ausente.json')
        cliente_id = salvar_cliente('João Silva', '51999999999', banco)
        assert listar_clientes(banco) == [(cliente_id, 'João Silva', '51999999999')]
        assert atualizar_cliente(cliente_id, 'João Atualizado', '51888888888', banco)
        assert listar_clientes(banco)[0][1] == 'João Atualizado'
        assert remover_cliente(cliente_id, banco)
        assert listar_clientes(banco) == []
        assert not remover_cliente(cliente_id, banco)
        cliente_id = salvar_cliente('Maria', caminho=banco)
        assert listar_clientes(banco) == [(cliente_id, 'Maria', None)]
        try:
            salvar_cliente(' ', caminho=banco)
        except ValueError:
            pass
        else:
            raise AssertionError('Nome vazio deveria ser recusado.')


def verificar_cliente_pedido():
    pedido = Pedido()
    cliente = (1, 'João Silva', '51999999999')
    pedido.definir_cliente(cliente)
    pedido.adicionar(Produto('P01', 'Mussarela', 4990), '1')
    comprovante = pedido.finalizar('PIX', pedido.versao())
    assert comprovante.cliente == cliente
    pedido.novo()
    assert pedido.cliente is None


def verificar_repositorio():
    with TemporaryDirectory() as pasta:
        repo = RepositorioSqlite(Path(pasta) / 'clientes.db')
        repo.iniciar()
        produto_id = repo.adicionar_produto('Arroz', 2590)
        cliente_id = repo.adicionar_cliente('João')
        assert repo.listar_produtos() == [(str(produto_id), 'Arroz', 2590)]
        assert repo.listar_clientes() == [(cliente_id, 'João', None)]
        repo.iniciar()
        assert len(repo.listar_clientes()) == 1
        assert listar_produtos(repo.caminho) == repo.listar_produtos()
        assert listar_clientes(repo.caminho) == repo.listar_clientes()


def verificar_csv():
    with TemporaryDirectory() as pasta:
        caminho = Path(pasta) / 'vendas.csv'
        formas = ['Débito; especial', 'Crédito "teste"', 'PIX']
        for forma in formas:
            registrar_venda_csv(Comprovante([], 2500, forma), caminho)
        with caminho.open(newline='', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=';')
            linhas = list(leitor)
        assert [linha['forma_pagamento'] for linha in linhas] == formas
        assert all(linha['total_reais'] == '25.00' for linha in linhas)
        datetime.strptime(linhas[0]['data_hora'], '%Y-%m-%d %H:%M:%S')
        exportar_csv(Path(pasta) / 'relatorio.csv', Comprovante([], 12345, 'Dinheiro'))


def verificar_perfis():
    sessao = SessaoDemo()
    sessao.entrar('João', 'Caixa')
    assert sessao.pode_operar_vendas()
    assert not sessao.pode_configurar()
    sessao.sair()
    assert not sessao.pode_operar_vendas()
    sessao.entrar('Ana', 'Administracao')
    assert sessao.pode_configurar()
    assert not sessao.pode_operar_vendas()


def verificar_pedido():
    pedido = Pedido()
    pedido.adicionar(Produto(1, 'Arroz', 2590), '2')
    assert pedido.total_centavos() == 5180
    comprovante = pedido.finalizar('PIX', pedido.versao())
    assert comprovante.total_centavos == 4507
    assert not pedido.aberto


def verificar_cadastro_controller():
    with TemporaryDirectory() as diretorio:
        repositorios = (
            RepositorioMemoria(),
            RepositorioSqlite(Path(diretorio) / "cadastro.db"),
        )
        for repositorio in repositorios:
            iniciar = getattr(repositorio, "iniciar", None)
            if iniciar:
                iniciar()
            controller = CadastroController(repositorio)
            codigo = controller.salvar("produto", "  Pão  ", "12,50")
            assert any(item[1:] == ("Pão", 1250) for item in controller.listar("produto"))
            assert controller.salvar("produto", "Pão integral", "15.00", codigo)
            assert not controller.excluir("produto", codigo, False)
            assert controller.excluir("produto", codigo, True)
            assert controller.listar("produto") == []
            cliente = controller.salvar("cliente", " Ana ")
            assert any(item[1] == "Ana" for item in controller.listar("cliente"))
            assert controller.salvar("cliente", "Ana Silva", codigo=cliente)
            assert not controller.excluir("cliente", cliente, False)
            assert controller.excluir("cliente", cliente, True)
            assert controller.listar("cliente") == []
            try:
                controller.salvar("produto", "Inválido", "0")
            except ValueError:
                pass
            else:
                raise AssertionError("Preço zero deveria ser recusado.")


def verificar_controller_produtos():
    with TemporaryDirectory() as diretorio:
        for repositorio in (ProdutosMemoria(), ProdutosSQLite(Path(diretorio) / "produtos.db")):
            iniciar = getattr(repositorio, "iniciar", None)
            if iniciar:
                iniciar()
            controller = ProdutoController(repositorio)
            controller.salvar_produto("P1", " Arroz ", 2590)
            assert ("P1", "Arroz", 2590) in controller.listar_produtos()
            assert controller.atualizar_produto("P1", "Feijão", 890)
            assert controller.remover_produto("P1")
            assert controller.listar_produtos() == []


def main():
    testes = [('SQLite', verificar_sqlite), ('Clientes', verificar_clientes), ('Cliente no pedido', verificar_cliente_pedido), ('Repositório', verificar_repositorio),
              ('CSV', verificar_csv), ('Perfis', verificar_perfis), ('Pedido', verificar_pedido), ('Cadastro A16', verificar_cadastro_controller), ('Controller de produtos A16', verificar_controller_produtos)]
    for nome, teste in testes:
        teste()
        print(f'OK: {nome}')
    print(f'{len(testes)} verificações concluídas.')


if __name__ == '__main__':
    main()

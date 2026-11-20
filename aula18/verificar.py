from pathlib import Path
from tempfile import TemporaryDirectory
from repositorio import RepositorioSqlite
from modelos import Produto, Pedido
from controller import CadastroController
from memoria import RepositorioMemoria
from pagamento import calcular_pagamento
import sqlite3


def verificar():
    with TemporaryDirectory() as pasta:
        repo = RepositorioSqlite(Path(pasta) / "teste.db")
        repo.iniciar()
        controller = CadastroController(repo)
        cliente = controller.salvar("cliente", "Lia")
        produto = controller.salvar("produto", "Sorvete", "6,50")
        pedido = Pedido()
        pedido.definir_cliente((cliente, "Lia", None))
        pedido.adicionar(Produto(str(produto), "Sorvete", 650), "2")
        venda, total = repo.registrar_venda(cliente, pedido.itens, "PIX")
        assert total == 1131
        assert len(repo.listar_vendas()) == 1
        assert not repo.excluir_produto(produto, confirmado=False)
        try:
            repo.excluir_produto(produto, confirmado=True)
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("Produto vinculado não pode ser excluído")
        try:
            repo.registrar_venda(cliente, [(produto, 1), ("AUSENTE", 1)], "PIX")
        except ValueError:
            pass
        else:
            raise AssertionError("Venda inválida deveria falhar")
        assert len(repo.listar_vendas()) == 1
        assert controller.listar("cliente")[0][1] == "Lia"
        memoria = RepositorioMemoria()
        cadastro = CadastroController(memoria)
        assert cadastro.salvar("cliente", "Rui") == 1
        assert cadastro.salvar("produto", "Picolé", "3,50") == 1
        assert cadastro.listar("produto")[0][2] == 350
    return True


if __name__ == "__main__":
    assert verificar()
    print("OK: cadastro, venda, rollback, vínculos e memória")

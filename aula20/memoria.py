# A16: assinaturas de apoio; traga sua implementação anterior.
from repositorio import RepositorioProdutos, validar_nome, validar_preco, validar_id


class ProdutosMemoria(RepositorioProdutos):
    """Repositório de produtos em memória com o mesmo contrato do SQLite."""

    def __init__(self):
        self.produtos = {}

    def listar(self):
        return list(self.produtos.values())

    def salvar(self, codigo, nome, preco):
        codigo = validar_id(codigo)
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        if codigo in self.produtos:
            raise ValueError(f"O produto '{codigo}' já existe.")
        self.produtos[codigo] = (codigo, nome, preco)

    def atualizar(self, codigo, nome, preco):
        codigo = validar_id(codigo)
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        if codigo not in self.produtos:
            return False
        self.produtos[codigo] = (codigo, nome, preco)
        return True

    def remover(self, codigo):
        codigo = validar_id(codigo)
        return self.produtos.pop(codigo, None) is not None


class RepositorioMemoria:
    def __init__(self):
        self.produtos = {}
        self.clientes = {}
        self.proximo_produto = 1
        self.proximo_cliente = 1

    def adicionar_produto(self, nome, preco):
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        codigo = self.proximo_produto
        self.produtos[codigo] = (codigo, nome, preco)
        self.proximo_produto += 1
        return codigo

    def listar_produtos(self):
        return list(self.produtos.values())

    def editar_produto(self, codigo, nome, preco):
        codigo = int(validar_id(codigo))
        nome = validar_nome(nome)
        preco = validar_preco(preco)
        if codigo not in self.produtos:
            return False
        self.produtos[codigo] = (codigo, nome, preco)
        return True

    def excluir_produto(self, codigo, confirmado=False):
        if not confirmado:
            return False
        codigo = int(validar_id(codigo))
        return self.produtos.pop(codigo, None) is not None

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        codigo = self.proximo_cliente
        self.clientes[codigo] = (codigo, nome, None)
        self.proximo_cliente += 1
        return codigo

    def listar_clientes(self):
        return list(self.clientes.values())

    def editar_cliente(self, codigo, nome):
        codigo = int(validar_id(codigo))
        nome = validar_nome(nome)
        if codigo not in self.clientes:
            return False
        self.clientes[codigo] = (codigo, nome, None)
        return True

    def excluir_cliente(self, codigo, confirmado=False):
        if not confirmado:
            return False
        codigo = int(validar_id(codigo))
        return self.clientes.pop(codigo, None) is not None

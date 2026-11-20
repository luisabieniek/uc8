# A16: assinaturas de apoio; traga sua implementação anterior.
from pagamento import preco_para_centavos
from repositorio import validar_id, validar_nome, validar_preco


class ProdutoController:
    """Valida e encaminha operações de produtos ao repositório."""

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_produtos(self):
        return self.repositorio.listar()

    def salvar_produto(self, codigo, nome, preco):
        return self.repositorio.salvar(validar_id(codigo), validar_nome(nome), validar_preco(preco))

    def atualizar_produto(self, codigo, nome, preco):
        return self.repositorio.atualizar(validar_id(codigo), validar_nome(nome), validar_preco(preco))

    def remover_produto(self, codigo):
        return self.repositorio.remover(validar_id(codigo))


class CadastroController:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar(self, tipo):
        if tipo == "produto":
            return self.repositorio.listar_produtos()
        if tipo == "cliente":
            return self.repositorio.listar_clientes()
        raise ValueError("Tipo deve ser produto ou cliente.")

    def salvar(self, tipo, nome, preco_texto='', codigo=None):
        nome = validar_nome(nome)
        if tipo == "produto":
            preco = preco_para_centavos(preco_texto)
            if codigo is None:
                return self.repositorio.adicionar_produto(nome, preco)
            return self.repositorio.editar_produto(codigo, nome, preco)
        if tipo == "cliente":
            if codigo is None:
                return self.repositorio.adicionar_cliente(nome)
            return self.repositorio.editar_cliente(codigo, nome)
        raise ValueError("Tipo deve ser produto ou cliente.")

    def excluir(self, tipo, codigo, confirmado):
        if not confirmado:
            return False
        codigo = validar_id(codigo)
        if tipo == "produto":
            return self.repositorio.excluir_produto(codigo, confirmado=True)
        if tipo == "cliente":
            return self.repositorio.excluir_cliente(codigo, confirmado=True)
        raise ValueError("Tipo deve ser produto ou cliente.")

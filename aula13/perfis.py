"""A13 — controle demonstrativo de sessão e perfil."""


class SessaoDemo:
    def __init__(self):
        self.nome = None
        self.perfil = None

    def entrar(self, nome, perfil):
        nome = str(nome).strip()

        if not nome:
            raise ValueError("Informe o nome da pessoa.")

        if perfil not in ("Caixa", "Administracao"):
            raise ValueError("Escolha o perfil Caixa ou Administração.")

        self.nome = nome
        self.perfil = perfil

    def pode_configurar(self):
        return self.perfil == "Administracao"

    def pode_operar_vendas(self):
        return self.perfil == "Caixa"

    def sair(self):
        self.nome = None
        self.perfil = None

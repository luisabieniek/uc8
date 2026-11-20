class SessaoDemo:
    def __init__(self):
        self.sair()

    def entrar(self, nome, perfil):
        nome = nome.strip()
        if not nome:
            raise ValueError("Informe um nome fictício.")
        if perfil not in ("Caixa", "Administracao"):
            raise ValueError("Selecione um perfil.")
        self.nome = nome
        self.perfil = perfil

    def sair(self):
        self.nome = ""
        self.perfil = ""

    def pode_operar_vendas(self):
        return self.perfil == "Caixa"

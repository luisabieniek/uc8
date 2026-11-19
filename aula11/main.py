import tkinter as tk
from tkinter import ttk, messagebox

from modelos import Pizza, Bebida, Pedido
from pagamento import formatar_dinheiro


produtos = [
    Pizza("P01", "Mussarela", "Média", 3500),
    Pizza("P02", "Portuguesa", "Grande", 4500),
    Bebida("B01", "Refrigerante", 600),
    Bebida("B02", "Água", 400)
]


def criar_janela():
    principal = tk.Tk()
    principal.title("Pizzaria")
    principal.geometry("750x600")

    pedido = Pedido()
    produto_selecionado = tk.StringVar()
    quantidade = tk.StringVar(value="1")
    forma_pagamento = tk.StringVar(value="PIX")

    produtos_por_codigo = {
        produto.codigo: produto for produto in produtos
    }

    # Catálogo
    quadro_catalogo = ttk.LabelFrame(
        principal,
        text="Cardápio"
    )
    quadro_catalogo.pack(fill="x", padx=10, pady=10)

    tabela_catalogo = ttk.Treeview(
        quadro_catalogo,
        columns=("codigo", "nome", "preco"),
        show="headings",
        height=4
    )

    tabela_catalogo.heading("codigo", text="Código")
    tabela_catalogo.heading("nome", text="Produto")
    tabela_catalogo.heading("preco", text="Preço")

    tabela_catalogo.column("codigo", width=100)
    tabela_catalogo.column("nome", width=250)
    tabela_catalogo.column("preco", width=120)

    tabela_catalogo.pack(fill="x", padx=5, pady=5)

    for produto in produtos:
        tabela_catalogo.insert(
            "",
            "end",
            iid=produto.codigo,
            values=(
                produto.codigo,
                produto.nome,
                formatar_dinheiro(
                    produto.preco_centavos / 100
                )
            )
        )

    # Dados do item
    quadro_item = ttk.Frame(principal)
    quadro_item.pack(fill="x", padx=10, pady=5)

    ttk.Label(
        quadro_item,
        text="Quantidade:"
    ).pack(side="left")

    campo_quantidade = ttk.Entry(
        quadro_item,
        textvariable=quantidade,
        width=8
    )
    campo_quantidade.pack(side="left", padx=5)

    # Pedido
    quadro_pedido = ttk.LabelFrame(
        principal,
        text="Pedido atual"
    )
    quadro_pedido.pack(fill="both", expand=True, padx=10, pady=10)

    tabela_pedido = ttk.Treeview(
        quadro_pedido,
        columns=("codigo", "nome", "quantidade", "subtotal"),
        show="headings"
    )

    tabela_pedido.heading("codigo", text="Código")
    tabela_pedido.heading("nome", text="Produto")
    tabela_pedido.heading("quantidade", text="Quantidade")
    tabela_pedido.heading("subtotal", text="Subtotal")

    tabela_pedido.column("codigo", width=80)
    tabela_pedido.column("nome", width=220)
    tabela_pedido.column("quantidade", width=100)
    tabela_pedido.column("subtotal", width=120)

    tabela_pedido.pack(fill="both", expand=True, padx=5, pady=5)

    texto_total = ttk.Label(
        principal,
        text="Total: R$ 0,00",
        font=("Arial", 12, "bold")
    )
    texto_total.pack(pady=5)

    # Atualização da tela
    def atualizar_tela():
        tabela_pedido.delete(*tabela_pedido.get_children())

        for item in pedido.itens:
            tabela_pedido.insert(
                "",
                "end",
                iid=item.produto.codigo,
                values=(
                    item.produto.codigo,
                    item.produto.nome,
                    item.quantidade,
                    formatar_dinheiro(item.subtotal() / 100)
                )
            )

        texto_total.config(
            text="Total: " + formatar_dinheiro(
                pedido.calcular_total() / 100
            )
        )

    # Seleção do produto
    def codigo_selecionado():
        selecao = tabela_catalogo.selection()

        if not selecao:
            raise ValueError("Selecione um produto do cardápio.")

        return selecao[0]

    # Adicionar produto
    def ao_adicionar():
        try:
            codigo = codigo_selecionado()
            quantidade_item = int(quantidade.get())

            produto = produtos_por_codigo[codigo]

            pedido.adicionar(produto, quantidade_item)
            atualizar_tela()

        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))

    # Atualizar quantidade
    def ao_atualizar():
        try:
            selecao = tabela_pedido.selection()

            if not selecao:
                raise ValueError("Selecione um item do pedido.")

            codigo = selecao[0]
            quantidade_item = int(quantidade.get())

            pedido.atualizar(codigo, quantidade_item)
            atualizar_tela()

        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))

    # Remover produto
    def ao_remover():
        try:
            selecao = tabela_pedido.selection()

            if not selecao:
                raise ValueError("Selecione um item do pedido.")

            pedido.remover(selecao[0])
            atualizar_tela()

        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))

    # Botões do pedido
    quadro_botoes = ttk.Frame(principal)
    quadro_botoes.pack(pady=5)

    ttk.Button(
        quadro_botoes,
        text="Adicionar",
        command=ao_adicionar
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes,
        text="Atualizar",
        command=ao_atualizar
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes,
        text="Remover",
        command=ao_remover
    ).pack(side="left", padx=5)

    # Pagamento
    quadro_pagamento = ttk.LabelFrame(
        principal,
        text="Pagamento"
    )
    quadro_pagamento.pack(fill="x", padx=10, pady=10)

    ttk.Label(
        quadro_pagamento,
        text="Forma de pagamento:"
    ).pack(side="left", padx=5)

    opcoes_pagamento = ttk.Combobox(
        quadro_pagamento,
        textvariable=forma_pagamento,
        values=["Dinheiro", "PIX", "Débito", "Crédito"],
        state="readonly",
        width=15
    )
    opcoes_pagamento.pack(side="left", padx=5)

    # Comprovante
    def mostrar_comprovante(comprovante):
        janela = tk.Toplevel(principal)
        janela.title("Comprovante")
        janela.geometry("400x400")

        ttk.Label(
            janela,
            text="COMPROVANTE DO PEDIDO",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        for item in comprovante.itens:
            texto = (
                f"{item['quantidade']}x {item['nome']} - "
                f"{formatar_dinheiro(item['subtotal'] / 100)}"
            )

            ttk.Label(janela, text=texto).pack(anchor="w", padx=15)

        ttk.Separator(janela).pack(fill="x", padx=10, pady=10)

        pagamento = comprovante.pagamento

        ttk.Label(
            janela,
            text=f"Forma: {pagamento['forma']}"
        ).pack(pady=3)

        ttk.Label(
            janela,
            text=f"Total: {formatar_dinheiro(pagamento['total'])}"
        ).pack(pady=3)

        ttk.Label(
            janela,
            text=f"Valor final: {formatar_dinheiro(pagamento['valor_final'])}",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        ttk.Button(
            janela,
            text="Fechar",
            command=janela.destroy
        ).pack(pady=10)

    # Prévia do pedido
    def abrir_previa():
        if not pedido.itens:
            messagebox.showwarning(
                "Pedido",
                "Adicione pelo menos um produto."
            )
            return

        versao_previa = pedido.versao()

        janela_previa = tk.Toplevel(principal)
        janela_previa.title("Prévia do pedido")
        janela_previa.geometry("400x350")

        ttk.Label(
            janela_previa,
            text="Confira seu pedido",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        for item in pedido.itens:
            ttk.Label(
                janela_previa,
                text=(
                    f"{item.quantidade}x {item.produto.nome} - "
                    f"{formatar_dinheiro(item.subtotal() / 100)}"
                )
            ).pack(anchor="w", padx=15)

        pagamento = forma_pagamento.get()

        try:
            from pagamento import calcular_pagamento

            resultado = calcular_pagamento(
                pedido.calcular_total(),
                pagamento
            )

        except ValueError as erro:
            messagebox.showwarning("Pagamento", str(erro))
            janela_previa.destroy()
            return

        ttk.Separator(janela_previa).pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            janela_previa,
            text=f"Forma: {pagamento}"
        ).pack()

        ttk.Label(
            janela_previa,
            text=f"Total: {formatar_dinheiro(resultado['total'])}"
        ).pack()

        ttk.Label(
            janela_previa,
            text=f"Valor final: {formatar_dinheiro(resultado['valor_final'])}",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        # Confirmar pedido
        def confirmar():
            try:
                comprovante = pedido.finalizar(
                    pagamento,
                    versao_previa
                )

                janela_previa.destroy()
                mostrar_comprovante(comprovante)
                atualizar_tela()

            except ValueError as erro:
                messagebox.showwarning("Pedido", str(erro))
                janela_previa.destroy()

        quadro_confirmacao = ttk.Frame(janela_previa)
        quadro_confirmacao.pack(pady=15)

        ttk.Button(
            quadro_confirmacao,
            text="Confirmar",
            command=confirmar
        ).pack(side="left", padx=5)

        ttk.Button(
            quadro_confirmacao,
            text="Cancelar",
            command=janela_previa.destroy
        ).pack(side="left", padx=5)

        janela_previa.bind(
            "<Escape>",
            lambda evento: janela_previa.destroy()
        )

    # Novo pedido
    def novo_pedido():
        if pedido.itens:
            resposta = messagebox.askyesno(
                "Novo pedido",
                "Deseja descartar o pedido atual?"
            )

            if not resposta:
                return

        pedido.novo()
        atualizar_tela()

    quadro_final = ttk.Frame(principal)
    quadro_final.pack(pady=10)

    ttk.Button(
        quadro_final,
        text="Conferir pedido",
        command=abrir_previa
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_final,
        text="Novo pedido",
        command=novo_pedido
    ).pack(side="left", padx=5)

    principal.mainloop()


if __name__ == "__main__":
    criar_janela()
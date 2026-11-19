# A09: integre sua versão anterior; preserve-a em outra pasta.

import tkinter as tk
from tkinter import ttk

from modelos import Produto, Pedido, formatar


def criar_janela():

    janela = tk.Tk()
    janela.title("Pedido")
    janela.geometry("700x650")

    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)

    pedido = Pedido()

    catalogo = [
        Produto("P1", "Picolé de fruta", 500),
        Produto("P2", "Picolé de leite", 750)
    ]

    grupo = ttk.LabelFrame(base, text="Pedido", padding=10)
    grupo.grid(row=0, column=0, sticky="nsew")
    grupo.columnconfigure(0, weight=1)

    ttk.Label(grupo, text="Catálogo fictício").grid(row=0, column=0, sticky="w")

    tabela_catalogo = ttk.Treeview(grupo, columns=("produto", "preco"), show="headings", height=4)

    tabela_catalogo.heading("produto", text="Produto")
    tabela_catalogo.heading("preco", text="Preço R$")

    tabela_catalogo.column("produto", width=260)
    tabela_catalogo.column("preco", width=120)

    tabela_catalogo.grid(row=1, column=0, sticky="ew", pady=4)

    for produto in catalogo:
        tabela_catalogo.insert(
            "",
            tk.END,
            iid=produto.codigo,
            values=(
                produto.nome,
                f"{produto.preco_centavos / 100:.2f}".replace(".", ",")
            )
        )

    ttk.Label(grupo, text="Quantidade inteira (1 a 999):").grid(
        row=2,
        column=0,
        sticky="w",
        pady=(8, 0)
    )

    entrada_quantidade = ttk.Entry(grupo)
    entrada_quantidade.grid(row=3, column=0, sticky="ew", pady=4)

    acoes = ttk.Frame(grupo)
    acoes.grid(row=4, column=0, sticky="w", pady=6)

    tabela_frame = ttk.Frame(grupo)
    tabela_frame.grid(row=5, column=0, sticky="nsew", pady=4)

    tabela_pedido = ttk.Treeview(
        tabela_frame,
        columns=("item", "quantidade", "subtotal"),
        show="headings",
        height=8
    )

    tabela_pedido.heading("item", text="Item")
    tabela_pedido.heading("quantidade", text="Quantidade")
    tabela_pedido.heading("subtotal", text="Subtotal R$")

    tabela_pedido.column("item", width=220)
    tabela_pedido.column("quantidade", width=120)
    tabela_pedido.column("subtotal", width=120)

    barra = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela_pedido.yview)

    tabela_pedido.configure(yscrollcommand=barra.set)

    tabela_pedido.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    ttk.Label(grupo, text="Forma de pagamento:").grid(
        row=6,
        column=0,
        sticky="w",
        pady=(10, 0)
    )

    pagamento = ttk.Combobox(
        grupo,
        state="readonly",
        values=["PIX", "Cartão Débito", "Cartão Crédito"]
    )

    pagamento.grid(row=7, column=0, sticky="ew")
    pagamento.current(0)

    total = ttk.Label(grupo, text="Total: R$ 0,00")
    total.grid(row=9, column=0, sticky="w", pady=8)

    previa = ttk.Label(grupo, text="Prévia: pedido preservado.")
    previa.grid(row=10, column=0, sticky="w", pady=8)

    def atualizar_tela():

        for item in tabela_pedido.get_children():
            tabela_pedido.delete(item)

        valor_total = 0

        for linha in pedido.linhas():

            tabela_pedido.insert(
                "",
                tk.END,
                values=(
                    linha["nome"],
                    linha["quantidade"],
                    formatar(linha["subtotal"]).replace("R$ ", "")
                )
            )

            valor_total += linha["subtotal"]

        total.configure(text=f"Total: {formatar(valor_total)}")

        if pagamento.get() == "PIX":

            desconto = round(valor_total * 0.13)

            previa.configure(
                text=f"Prévia: desconto {formatar(desconto)}; total {formatar(valor_total - desconto)}. Pedido preservado."
            )

        else:

            previa.configure(
                text=f"Prévia: total {formatar(valor_total)}."
            )

    def ao_adicionar():

        selecionado = tabela_catalogo.selection()

        if not selecionado:
            return

        codigo = selecionado[0]

        produto = next(
            p for p in catalogo
            if p.codigo == codigo
        )

        pedido.adicionar(produto, entrada_quantidade.get())

        atualizar_tela()

    def ao_atualizar():

        selecionado = tabela_catalogo.selection()

        if not selecionado:
            return

        pedido.atualizar(
            selecionado[0],
            entrada_quantidade.get()
        )

        atualizar_tela()

    def ao_remover():

        selecionado = tabela_catalogo.selection()

        if not selecionado:
            return

        pedido.remover(
            selecionado[0]
        )

        atualizar_tela()

    ttk.Button(acoes, text="Adicionar", command=ao_adicionar).grid(row=0, column=0, padx=3)

    ttk.Button(
        acoes,
        text="Atualizar quantidade",
        command=ao_atualizar
    ).grid(row=0, column=1, padx=3)

    ttk.Button(
        acoes,
        text="Remover",
        command=ao_remover
    ).grid(row=0, column=2, padx=3)

    ttk.Button(
        grupo,
        text="Conferir pagamento",
        command=atualizar_tela
    ).grid(row=8, column=0, sticky="w", pady=8)

    entrada_quantidade.focus_set()

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
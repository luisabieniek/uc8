
import tkinter as tk
from tkinter import ttk
from decimal import Decimal
from modelos import Pizza, Bebida, Pedido, formatar
from pagamentos import calcular_pagamento, FATORES


CATALOGO = [
    Pizza("PM1", "Mussarela", "Media", 3500),
    Pizza("PG1", "Mussarela", "Grande", 4500),
    Pizza("PM2", "Calabresa", "Media", 3800),
    Pizza("PG2", "Calabresa", "Grande", 4800),
    Pizza("PM3", "Frango", "Media", 3600),
    Pizza("PG3", "Frango", "Grande", 4600),
    Bebida("B01", "Suco", 600),
    Bebida("B02", "Refrigerante", 500),
    Bebida("B03", "Agua", 300),
]


def label_catalogo(produto):
    tamanho = f" ({produto.tamanho})" if isinstance(produto, Pizza) else ""
    return f"{produto.codigo}  {produto.nome}{tamanho}  {formatar(produto.preco_centavos)}"


def redesenhar(tree, lbl_total, pedido):
    tree.delete(*tree.get_children())

    for item in pedido.itens:
        tamanho = item.produto.tamanho if isinstance(item.produto, Pizza) else "-"

        tree.insert(
            "",
            tk.END,
            iid=item.produto.codigo,
            values=(
                item.produto.codigo,
                item.produto.nome,
                tamanho,
                item.quantidade,
                formatar(item.subtotal())
            )
        )

    total = pedido.total_centavos()
    lbl_total.configure(text=f"Total: {formatar(total)}")


def codigo_selecionado(tree):
    selecao = tree.selection()

    if not selecao:
        return None

    return selecao[0]


def criar_janela():
    janela = tk.Tk()
    janela.title("Pizzaria — A10")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)

    pedido = Pedido()

    grupo_catalogo = ttk.LabelFrame(
        base, text="Catalogo", padding=10
    )
    grupo_catalogo.grid(row=0, column=0, sticky="ew", pady=4)
    grupo_catalogo.columnconfigure(0, weight=1)

    rotulos = [label_catalogo(produto) for produto in CATALOGO]

    combo_produto = ttk.Combobox(
        grupo_catalogo,
        values=rotulos,
        state="readonly"
    )
    combo_produto.grid(row=0, column=0, padx=6, pady=4, sticky="ew")
    combo_produto.current(0)

    grupo_quantidade = ttk.LabelFrame(
        base, text="Quantidade", padding=10
    )
    grupo_quantidade.grid(row=1, column=0, sticky="ew", pady=4)
    grupo_quantidade.columnconfigure(1, weight=1)

    ttk.Label(grupo_quantidade, text="Quantidade:").grid(
        row=0, column=0, padx=6, pady=4, sticky="w"
    )

    entrada_qtd = ttk.Entry(grupo_quantidade)
    entrada_qtd.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

    acoes = ttk.Frame(base, padding=5)
    acoes.grid(row=2, column=0, sticky="ew", pady=4)

    acoes.columnconfigure((0, 1, 2), weight=1)

    grupo_pedido = ttk.LabelFrame(
        base, text="Pedido", padding=10
    )
    grupo_pedido.grid(row=3, column=0, sticky="nsew", pady=4)
    grupo_pedido.columnconfigure(0, weight=1)
    grupo_pedido.rowconfigure(0, weight=1)
    base.rowconfigure(3, weight=1)

    colunas = ("codigo", "nome", "tamanho", "qtd", "subtotal")

    tree = ttk.Treeview(
        grupo_pedido,
        columns=colunas,
        show="headings",
        height=6,
        selectmode="browse"
    )

    tree.heading("codigo", text="Codigo")
    tree.heading("nome", text="Nome")
    tree.heading("tamanho", text="Tamanho")
    tree.heading("qtd", text="Qtd")
    tree.heading("subtotal", text="Subtotal")

    tree.column("codigo", width=55, anchor="center")
    tree.column("nome", width=110, anchor="w")
    tree.column("tamanho", width=70, anchor="center")
    tree.column("qtd", width=45, anchor="center")
    tree.column("subtotal", width=95, anchor="e")

    tree.grid(row=0, column=0, sticky="nsew")

    scroll = ttk.Scrollbar(
        grupo_pedido,
        orient="vertical",
        command=tree.yview
    )
    scroll.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scroll.set)

    lbl_total = ttk.Label(
        base,
        text="Total: R$ 0,00",
        font=("", 10, "bold")
    )
    lbl_total.grid(row=4, column=0, sticky="e", padx=4, pady=4)

    grupo_pagamento = ttk.LabelFrame(
        base, text="Previa de pagamento", padding=10
    )
    grupo_pagamento.grid(row=5, column=0, sticky="ew", pady=4)
    grupo_pagamento.columnconfigure(1, weight=1)

    ttk.Label(grupo_pagamento, text="Forma:").grid(
        row=0, column=0, padx=6, pady=4, sticky="w"
    )

    combo_forma = ttk.Combobox(
        grupo_pagamento,
        values=list(FATORES.keys()),
        state="readonly"
    )
    combo_forma.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
    combo_forma.current(0)

    lbl_previa = ttk.Label(
        grupo_pagamento,
        text="",
        wraplength=380
    )
    lbl_previa.grid(row=1, column=0, columnspan=2, padx=6, pady=4, sticky="w")

    def ao_adicionar():
        produto = CATALOGO[combo_produto.current()]
        quantidade = entrada_qtd.get()

        try:
            pedido.adicionar(produto, quantidade)

            aviso.configure(
                text=f"Adicionado: {produto.nome} x{quantidade}"
            )

            redesenhar(tree, lbl_total, pedido)
            entrada_qtd.delete(0, tk.END)

        except (ValueError, RuntimeError) as e:
            aviso.configure(text=f"Recusado: {e}")

        entrada_qtd.focus_set()

    def ao_atualizar():
        codigo = codigo_selecionado(tree)

        if not codigo:
            aviso.configure(text="Selecione um item na tabela para atualizar.")
            return

        quantidade = entrada_qtd.get()

        try:
            pedido.atualizar(codigo, quantidade)

            aviso.configure(
                text=f"Atualizado: {codigo} -> x{quantidade}"
            )

            redesenhar(tree, lbl_total, pedido)
            entrada_qtd.delete(0, tk.END)

        except (ValueError, RuntimeError) as e:
            aviso.configure(text=f"Recusado: {e}")

        entrada_qtd.focus_set()

    def ao_remover():
        codigo = codigo_selecionado(tree)

        if not codigo:
            aviso.configure(text="Selecione um item na tabela para remover.")
            return

        try:
            pedido.remover(codigo)

            aviso.configure(text=f"Removido: {codigo}")
            redesenhar(tree, lbl_total, pedido)

        except (ValueError, RuntimeError) as e:
            aviso.configure(text=f"Recusado: {e}")

    def ao_calcular_previa():
        if not pedido.itens:
            aviso.configure(text="Pedido vazio. Adicione itens antes de calcular.")
            return

        subtotal = str(Decimal(pedido.total_centavos()) / 100)
        forma = combo_forma.get()

        try:
            total, desconto = calcular_pagamento(subtotal, forma)

            lbl_previa.configure(
                text=f"{forma}: total {formatar(total)}  desconto {formatar(desconto)}"
            )

            aviso.configure(
                text="Previa calculada. Pedido nao foi alterado."
            )

        except ValueError as e:
            lbl_previa.configure(text="")
            aviso.configure(text=f"Recusado: {e}")

    ttk.Button(
        acoes, text="Adicionar", command=ao_adicionar
    ).grid(row=0, column=0, padx=4, pady=6, sticky="ew")

    ttk.Button(
        acoes, text="Atualizar", command=ao_atualizar
    ).grid(row=0, column=1, padx=4, pady=6, sticky="ew")

    ttk.Button(
        acoes, text="Remover", command=ao_remover
    ).grid(row=0, column=2, padx=4, pady=6, sticky="ew")

    ttk.Button(
        grupo_pagamento,
        text="Calcular previa",
        command=ao_calcular_previa
    ).grid(row=2, column=0, columnspan=2, pady=6)

    entrada_qtd.bind("<Return>", lambda event: ao_adicionar())
    tree.bind("<Return>", lambda event: ao_atualizar())
    tree.bind("<Delete>", lambda event: ao_remover())

    aviso = ttk.Label(
        base,
        text="Selecione um produto e informe a quantidade.",
        wraplength=430
    )
    aviso.grid(row=6, column=0, pady=6, sticky="w")

    combo_produto.focus_set()

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

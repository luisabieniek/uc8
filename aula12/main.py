
"""A12 — interface da pizzaria com catálogo JSON."""

import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from decimal import Decimal

from arquivos import ler_catalogo, salvar_catalogo, validar_catalogo
from modelos import Pedido, Produto, formatar
from pagamento import calcular_pagamento, FATORES


def criar_janela():
    janela = tk.Tk()
    janela.title("Pizzaria — A12")
    janela.geometry("680x720")
    janela.minsize(540, 580)

    caminho_padrao = Path(__file__).with_name("catalogo.json")
    catalogo = []
    pedido = Pedido()

    # Abas
    notebook = ttk.Notebook(janela)
    notebook.pack(fill="both", expand=True)

    aba_pedido = ttk.Frame(notebook, padding=12)
    aba_catalogo = ttk.Frame(notebook, padding=12)

    notebook.add(aba_pedido, text="Pedido")
    notebook.add(aba_catalogo, text="Catálogo JSON")

    # Menu de navegação
    menu = tk.Menu(janela)
    menu_navegacao = tk.Menu(menu, tearoff=False)

    menu_navegacao.add_command(
        label="Pedido",
        command=lambda: notebook.select(aba_pedido)
    )

    menu_navegacao.add_command(
        label="Catálogo JSON",
        command=lambda: notebook.select(aba_catalogo)
    )

    menu.add_cascade(label="Navegar", menu=menu_navegacao)
    janela.configure(menu=menu)

    janela.bind_all(
        "<Control-Key-1>",
        lambda evento: notebook.select(aba_pedido)
    )
    janela.bind_all(
        "<Control-Key-2>",
        lambda evento: notebook.select(aba_catalogo)
    )

    # Catálogo inicial
    aviso_inicial = "Selecione um produto e informe a quantidade."
    texto_inicial = None

    try:
        dados = ler_catalogo(caminho_padrao)

        if dados is None:
            aviso_inicial = "Catálogo ausente. Carregue um JSON."

        else:
            catalogo = [
                Produto(
                    item["id"],
                    item["nome"],
                    item["preco_centavos"]
                )
                for item in dados
            ]

    except (ValueError, OSError) as erro:
        aviso_inicial = f"Catálogo inválido: {erro}"

        try:
            texto_inicial = caminho_padrao.read_text(
                encoding="utf-8"
            )
        except (OSError, UnicodeDecodeError):
            pass

    # Estrutura da aba Pedido
    aba_pedido.columnconfigure(0, weight=1)
    aba_pedido.rowconfigure(3, weight=1)

    # Catálogo
    grupo_catalogo = ttk.LabelFrame(
        aba_pedido,
        text="Catálogo",
        padding=6
    )
    grupo_catalogo.grid(
        row=0, column=0, sticky="ew", pady=4
    )
    grupo_catalogo.columnconfigure(0, weight=1)

    opcoes_produtos = []

    combo_produto = ttk.Combobox(
        grupo_catalogo,
        values=opcoes_produtos,
        state="readonly"
    )
    combo_produto.grid(
        row=0, column=0, sticky="ew", padx=4, pady=4
    )

    def atualizar_opcoes_catalogo():
        opcoes = []

        for produto in catalogo:
            opcoes.append(
                f"{produto.codigo} {produto.nome} "
                f"{formatar(produto.preco_centavos)}"
            )

        combo_produto.configure(values=opcoes)

        if opcoes:
            combo_produto.current(0)
        else:
            combo_produto.set("")

    atualizar_opcoes_catalogo()

    # Quantidade
    grupo_quantidade = ttk.LabelFrame(
        aba_pedido,
        text="Quantidade",
        padding=6
    )
    grupo_quantidade.grid(
        row=1, column=0, sticky="ew", pady=4
    )
    grupo_quantidade.columnconfigure(1, weight=1)

    ttk.Label(
        grupo_quantidade,
        text="Qtd:"
    ).grid(row=0, column=0, padx=6, pady=4)

    entrada_quantidade = ttk.Entry(grupo_quantidade)
    entrada_quantidade.grid(
        row=0, column=1, padx=6, pady=4, sticky="ew"
    )

    # Tabela do pedido
    grupo_pedido = ttk.LabelFrame(
        aba_pedido,
        text="Pedido",
        padding=6
    )
    grupo_pedido.grid(
        row=3, column=0, sticky="nsew", pady=4
    )
    grupo_pedido.columnconfigure(0, weight=1)
    grupo_pedido.rowconfigure(0, weight=1)

    colunas = ("codigo", "nome", "quantidade", "subtotal")

    tree = ttk.Treeview(
        grupo_pedido,
        columns=colunas,
        show="headings",
        height=6,
        selectmode="browse"
    )

    tree.heading("codigo", text="Código")
    tree.heading("nome", text="Nome")
    tree.heading("quantidade", text="Qtd")
    tree.heading("subtotal", text="Subtotal")

    tree.column("codigo", width=65, anchor="center")
    tree.column("nome", width=150)
    tree.column("quantidade", width=50, anchor="center")
    tree.column("subtotal", width=100, anchor="e")

    tree.grid(row=0, column=0, sticky="nsew")

    barra = ttk.Scrollbar(
        grupo_pedido,
        orient="vertical",
        command=tree.yview
    )
    barra.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=barra.set)

    # Total e aviso
    lbl_total = ttk.Label(
        aba_pedido,
        text="Total: R$ 0,00",
        font=("", 10, "bold")
    )
    lbl_total.grid(row=4, column=0, sticky="e", pady=4)

    aviso = ttk.Label(
        aba_pedido,
        text=aviso_inicial,
        wraplength=500
    )
    aviso.grid(row=6, column=0, sticky="w", pady=6)

    # Atualizar tabela
    def redesenhar():
        tree.delete(*tree.get_children())

        for item in pedido.itens:
            tree.insert(
                "",
                tk.END,
                iid=item.produto.codigo,
                values=(
                    item.produto.codigo,
                    item.produto.nome,
                    item.quantidade,
                    formatar(item.subtotal())
                )
            )

        total = pedido.total_centavos()
        lbl_total.configure(text=f"Total: {formatar(total)}")

    def codigo_selecionado():
        selecao = tree.selection()
        return selecao[0] if selecao else None

    # Adicionar
    def ao_adicionar():
        indice = combo_produto.current()

        if not 0 <= indice < len(catalogo):
            aviso.configure(
                text="Selecione um produto do catálogo."
            )
            return

        produto = catalogo[indice]

        try:
            pedido.adicionar(
                produto,
                entrada_quantidade.get()
            )

            redesenhar()
            aviso.configure(text=f"Produto adicionado: {produto.nome}")
            entrada_quantidade.delete(0, tk.END)

        except (ValueError, RuntimeError) as erro:
            aviso.configure(text=f"Recusado: {erro}")

        entrada_quantidade.focus_set()

    # Atualizar
    def ao_atualizar():
        codigo = codigo_selecionado()

        if codigo is None:
            aviso.configure(
                text="Selecione um item do pedido."
            )
            return

        try:
            pedido.atualizar(
                codigo,
                entrada_quantidade.get()
            )

            redesenhar()
            aviso.configure(text="Quantidade atualizada.")
            entrada_quantidade.delete(0, tk.END)

        except (ValueError, RuntimeError) as erro:
            aviso.configure(text=f"Recusado: {erro}")

        entrada_quantidade.focus_set()

    # Remover
    def ao_remover():
        codigo = codigo_selecionado()

        if codigo is None:
            aviso.configure(
                text="Selecione um item para remover."
            )
            return

        try:
            pedido.remover(codigo)
            redesenhar()
            aviso.configure(text="Produto removido.")

        except (ValueError, RuntimeError) as erro:
            aviso.configure(text=f"Recusado: {erro}")

    # Botões de montagem
    acoes = ttk.Frame(aba_pedido)
    acoes.grid(row=2, column=0, sticky="ew", pady=4)

    for coluna in range(3):
        acoes.columnconfigure(coluna, weight=1)

    ttk.Button(
        acoes,
        text="Adicionar",
        command=ao_adicionar
    ).grid(row=0, column=0, padx=4, sticky="ew")

    ttk.Button(
        acoes,
        text="Atualizar",
        command=ao_atualizar
    ).grid(row=0, column=1, padx=4, sticky="ew")

    ttk.Button(
        acoes,
        text="Remover",
        command=ao_remover
    ).grid(row=0, column=2, padx=4, sticky="ew")

    entrada_quantidade.bind(
        "<Return>",
        lambda evento: ao_adicionar()
    )

    tree.bind(
        "<Return>",
        lambda evento: ao_atualizar()
    )

    tree.bind(
        "<Delete>",
        lambda evento: ao_remover()
    )

    # Forma de pagamento
    grupo_pagamento = ttk.LabelFrame(
        aba_pedido,
        text="Pagamento",
        padding=6
    )
    grupo_pagamento.grid(
        row=5, column=0, sticky="ew", pady=4
    )
    grupo_pagamento.columnconfigure(1, weight=1)

    ttk.Label(
        grupo_pagamento,
        text="Forma:"
    ).grid(row=0, column=0, padx=6, pady=4)

    combo_forma = ttk.Combobox(
        grupo_pagamento,
        values=list(FATORES.keys()),
        state="readonly"
    )
    combo_forma.grid(
        row=0, column=1, padx=6, pady=4, sticky="ew"
    )
    combo_forma.current(0)

    # Comprovante
    def mostrar_comprovante(comprovante):
        top = tk.Toplevel(janela)
        top.title("Comprovante")
        top.resizable(False, False)

        frame = ttk.Frame(top, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Pedido confirmado",
            font=("", 10, "bold")
        ).pack(anchor="w", pady=5)

        for linha in comprovante.linhas:
            ttk.Label(
                frame,
                text=linha,
                wraplength=340
            ).pack(anchor="w")

        ttk.Separator(frame).pack(
            fill="x", pady=8
        )

        ttk.Label(
            frame,
            text=f"Forma: {comprovante.forma}"
        ).pack(anchor="w")

        ttk.Label(
            frame,
            text=(
                "Total com desconto: "
                f"{formatar(comprovante.total_centavos)}"
            )
        ).pack(anchor="w")

        aviso.configure(
            text="Pedido confirmado. Inicie um novo pedido."
        )

        def fechar():
            top.destroy()
            combo_produto.focus_set()

        ttk.Button(
            frame,
            text="Fechar",
            command=fechar
        ).pack(pady=8)

        top.protocol("WM_DELETE_WINDOW", fechar)
        top.bind("<Escape>", lambda evento: fechar())
        top.grab_set()

    # Prévia
    def abrir_previa():
        if not pedido.itens:
            aviso.configure(
                text="Pedido vazio. Adicione itens antes de confirmar."
            )
            return

        forma = combo_forma.get()
        versao_previa = pedido.versao()

        subtotal = str(Decimal(pedido.total_centavos()) / 100)

        try:
            total, desconto = calcular_pagamento(
                subtotal,
                forma
            )
        except ValueError as erro:
            aviso.configure(text=f"Recusado: {erro}")
            return

        top = tk.Toplevel(janela)
        top.title("Confirmar pedido")
        top.resizable(False, False)
        top.transient(janela)

        frame = ttk.Frame(top, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Resumo do pedido",
            font=("", 10, "bold")
        ).pack(anchor="w", pady=5)

        for linha in pedido.linhas():
            ttk.Label(
                frame,
                text=linha,
                wraplength=340
            ).pack(anchor="w")

        ttk.Separator(frame).pack(fill="x", pady=8)

        ttk.Label(frame, text=f"Forma: {forma}").pack(anchor="w")
        ttk.Label(
            frame,
            text=f"Total com desconto: {formatar(total)}"
        ).pack(anchor="w")
        ttk.Label(
            frame,
            text=f"Desconto: {formatar(desconto)}"
        ).pack(anchor="w")

        def confirmar():
            try:
                comprovante = pedido.finalizar(
                    forma,
                    versao_previa
                )

                top.destroy()
                mostrar_comprovante(comprovante)

            except (ValueError, RuntimeError) as erro:
                top.destroy()
                aviso.configure(text=f"Recusado: {erro}")

        def cancelar():
            top.destroy()
            aviso.configure(
                text="Confirmação cancelada. Pedido preservado."
            )

        botoes = ttk.Frame(frame)
        botoes.pack(fill="x", pady=10)

        ttk.Button(
            botoes,
            text="Confirmar",
            command=confirmar
        ).pack(side="left", expand=True, fill="x", padx=3)

        botao_cancelar = ttk.Button(
            botoes,
            text="Cancelar",
            command=cancelar
        )
        botao_cancelar.pack(
            side="left", expand=True, fill="x", padx=3
        )

        top.protocol("WM_DELETE_WINDOW", cancelar)
        top.bind("<Escape>", lambda evento: cancelar())

        botao_cancelar.focus_set()
        top.grab_set()

    # Novo pedido
    def ao_novo_pedido():
        if pedido.itens:
            resposta = messagebox.askyesno(
                "Novo pedido",
                "Deseja descartar a montagem atual?"
            )

            if not resposta:
                aviso.configure(
                    text="Pedido atual preservado."
                )
                return

        pedido.novo()
        redesenhar()
        aviso.configure(text="Novo pedido iniciado.")

    # Botões de pagamento
    botoes_pagamento = ttk.Frame(grupo_pagamento)
    botoes_pagamento.grid(
        row=1, column=0, columnspan=2, sticky="ew", pady=5
    )

    botoes_pagamento.columnconfigure(0, weight=1)
    botoes_pagamento.columnconfigure(1, weight=1)

    ttk.Button(
        botoes_pagamento,
        text="Confirmar pedido",
        command=abrir_previa
    ).grid(row=0, column=0, padx=3, sticky="ew")

    ttk.Button(
        botoes_pagamento,
        text="Novo pedido",
        command=ao_novo_pedido
    ).grid(row=0, column=1, padx=3, sticky="ew")

    # Aba Catálogo JSON
    aba_catalogo.columnconfigure(0, weight=1)
    aba_catalogo.rowconfigure(2, weight=1)

    ttk.Label(
        aba_catalogo,
        text="Arquivo do catálogo (JSON):"
    ).grid(row=0, column=0, sticky="w")

    caminho_json = tk.StringVar(value=str(caminho_padrao))

    linha_caminho = ttk.Frame(aba_catalogo)
    linha_caminho.grid(
        row=1, column=0, sticky="ew", pady=6
    )
    linha_caminho.columnconfigure(0, weight=1)

    entrada_caminho = ttk.Entry(
        linha_caminho,
        textvariable=caminho_json
    )
    entrada_caminho.grid(
        row=0, column=0, sticky="ew", padx=4
    )

    botoes_json = ttk.Frame(linha_caminho)
    botoes_json.grid(row=0, column=1)

    editor = ScrolledText(
        aba_catalogo,
        height=18,
        width=70,
        wrap="none",
        undo=True
    )
    editor.grid(
        row=2, column=0, sticky="nsew"
    )

    aviso_catalogo = ttk.Label(
        aba_catalogo,
        text="Edite uma lista JSON com id, nome e preco_centavos.",
        wraplength=600
    )
    aviso_catalogo.grid(
        row=3, column=0, sticky="w", pady=8
    )

    def definir_editor(dados):
        editor.delete("1.0", tk.END)

        editor.insert(
            "1.0",
            json.dumps(
                dados,
                ensure_ascii=False,
                indent=4
            )
        )

        editor.edit_modified(False)

    def atualizar_catalogo(dados):
        nonlocal catalogo

        codigo_atual = None
        indice = combo_produto.current()

        if 0 <= indice < len(catalogo):
            codigo_atual = catalogo[indice].codigo

        catalogo = [
            Produto(
                item["id"],
                item["nome"],
                item["preco_centavos"]
            )
            for item in dados
        ]

        atualizar_opcoes_catalogo()

        codigos = [
            produto.codigo for produto in catalogo
        ]

        if codigo_atual in codigos:
            combo_produto.current(codigos.index(codigo_atual))

    def obter_caminho():
        texto = caminho_json.get().strip()

        if not texto:
            aviso_catalogo.configure(
                text="Informe o caminho do arquivo."
            )
            return None

        caminho = Path(texto)

        if not caminho.is_absolute():
            caminho = Path(__file__).parent / caminho

        return caminho

    # Carregar catálogo
    def ao_carregar_catalogo():
        caminho = obter_caminho()

        if caminho is None:
            return

        if editor.edit_modified():
            resposta = messagebox.askyesno(
                "Descartar edição?",
                "Deseja descartar as alterações do editor?"
            )

            if not resposta:
                aviso_catalogo.configure(
                    text="Carregamento cancelado. Edição preservada."
                )
                return

        try:
            dados = ler_catalogo(caminho)

        except (ValueError, OSError) as erro:
            try:
                texto = caminho.read_text(encoding="utf-8")
                editor.delete("1.0", tk.END)
                editor.insert("1.0", texto)
                editor.edit_modified(False)
            except (OSError, UnicodeDecodeError):
                pass

            aviso_catalogo.configure(
                text=f"Catálogo inválido ou inacessível: {erro}"
            )
            return

        if dados is None:
            dados = []
            mensagem = "Arquivo ausente. Catálogo vazio carregado."
        else:
            mensagem = (
                f"Catálogo carregado: {len(dados)} produto(s)."
            )

        definir_editor(dados)
        atualizar_catalogo(dados)

        aviso_catalogo.configure(
            text=mensagem + " Pedido preservado."
        )

    # Salvar catálogo
    def ao_salvar_catalogo():
        caminho = obter_caminho()

        if caminho is None:
            return

        try:
            dados = json.loads(
                editor.get("1.0", "end-1c")
            )

            validar_catalogo(dados)

        except (json.JSONDecodeError, ValueError) as erro:
            aviso_catalogo.configure(
                text=f"Catálogo inválido. Arquivo não alterado: {erro}"
            )
            return

        acao = "Substituir" if caminho.exists() else "Criar"

        resposta = messagebox.askyesno(
            "Confirmar salvamento",
            f"{acao} o catálogo neste caminho?\n{caminho}"
        )

        if not resposta:
            aviso_catalogo.configure(
                text="Salvamento cancelado. Dados preservados."
            )
            return

        try:
            salvar_catalogo(caminho, dados)

        except (OSError, ValueError) as erro:
            aviso_catalogo.configure(
                text=f"Erro ao salvar: {erro}"
            )
            return

        definir_editor(dados)
        atualizar_catalogo(dados)

        aviso_catalogo.configure(
            text=f"Catálogo salvo: {len(dados)} produto(s). Pedido preservado."
        )

    ttk.Button(
        botoes_json,
        text="Carregar",
        command=ao_carregar_catalogo
    ).pack(side="left", padx=3)

    ttk.Button(
        botoes_json,
        text="Salvar",
        command=ao_salvar_catalogo
    ).pack(side="left", padx=3)

    # Teclas de navegação no editor
    editor.bind(
        "<Tab>",
        lambda evento: (
            evento.widget.tk_focusNext().focus_set(),
            "break"
        )[1]
    )

    editor.bind(
        "<Shift-Tab>",
        lambda evento: (
            evento.widget.tk_focusPrev().focus_set(),
            "break"
        )[1]
    )

    # Conteúdo inicial do editor
    if texto_inicial is not None:
        editor.insert("1.0", texto_inicial)
        editor.edit_modified(False)
    else:
        dados_iniciais = [
            {
                "id": produto.codigo,
                "nome": produto.nome,
                "preco_centavos": produto.preco_centavos
            }
            for produto in catalogo
        ]
        definir_editor(dados_iniciais)

    if catalogo:
        combo_produto.focus_set()
    else:
        notebook.select(aba_catalogo)

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

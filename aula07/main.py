# A07: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk, messagebox
from modelos import Produto, Pedido, formatar


def abrir_consulta(principal, pedido):
    if len(pedido.itens) == 0:
        messagebox.showinfo("Consulta do pedido", "Nenhum item adicionado nesta sessão.",
                            parent=principal
        )
        return None

    consulta = tk.Toplevel(principal)
    consulta.title("Consulta do pedido")

    texto = "\n".join(pedido.linhas())
    texto += f"\n\nTotal: {formatar(pedido.total_centavos())}"

    tk.Label(consulta, text=texto, justify="left", padx=10, pady=10).pack(fill="both", expand=True)
    tk.Button(consulta, text="Fechar", command=consulta.destroy).pack(pady=10)

    consulta.transient(principal)
    consulta.grab_set()
    consulta.focus_force()

    consulta.bind("<Escape>", lambda event: consulta.destroy())

    return consulta



def criar_janela():
    janela = tk.Tk()
    janela.title("Sorveteria - A07")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(1, weight=1)

    pedido = Pedido()
    fruta = Produto("F01", "Fruta", 500)
    leite = Produto("L01", "Leite", 750)

    catalogo = {
        "Fruta": fruta,
        "Leite": leite
    }

    grupo_produto = ttk.LabelFrame(
        base,
        text="Produto",
        padding=10
    )

    grupo_produto.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="nsew",
        pady=4
    )

    ttk.Label(grupo_produto, text="Produto:").grid(row=0, column=0, padx=6, pady=4)
    combo_produto = ttk.Combobox(grupo_produto,values=list(catalogo.keys()), state="readonly"    )
    combo_produto.grid(row=0, column=1, padx=6, pady=4, sticky="ew"    )
    combo_produto.current(0)
    ttk.Label(grupo_produto, text="Quantidade:").grid(row=1, column=0, padx=6, pady=4)
    entrada_quantidade = ttk.Entry(grupo_produto)
    entrada_quantidade.grid(row=1, column=1, padx=6, pady=4, sticky="ew"    )
    grupo_produto.columnconfigure(1, weight=1)
    aviso = ttk.Label(base, text="Use Fruta e Leite para testar.")
    aviso.grid(row=1, column=0, columnspan=2, sticky="w", pady=4)
    resultado = ttk.Label(base, text="Nenhum item adicionado.")
    resultado.grid(row=2, column=0, columnspan=2, sticky="w", pady=4)

    def atualizar_resultado():
        texto = "\n".join(pedido.linhas())

        if texto:
            texto += (
                f"\nTotal: "
                f"{formatar(pedido.total_centavos())}"
            )
        else:
            texto = "Nenhum item adicionado."

        resultado.configure(text=texto)

    def testar():
        try:
            produto = catalogo[
                combo_produto.get()
            ]

            pedido.adicionar(
                produto,
                entrada_quantidade.get()
            )

            aviso.configure(
                text="Item adicionado com sucesso."
            )

            atualizar_resultado()

            entrada_quantidade.delete(
                0,
                tk.END
            )

            entrada_quantidade.focus_set()

        except ValueError as erro:
            aviso.configure(text=str(erro))
            entrada_quantidade.focus_set()

    def ao_exibir():
        abrir_consulta(janela, pedido)

    def ao_limpar():
        entrada_quantidade.delete(0, tk.END)

        aviso.configure(
            text="Campo limpo."
        )

        entrada_quantidade.focus_set()

    ttk.Button(base, text="Adicionar", command=testar).grid(row=3, column=0, pady=6)
    ttk.Button(base, text="Consultar", command=ao_exibir).grid(row=3, column=1, pady=6)
    ttk.Button(base, text="Limpar campo", command=ao_limpar).grid(row=4, column=0, columnspan=2, pady=6)
    entrada_quantidade.focus_set()

    return janela



if __name__ == "__main__":
    criar_janela().mainloop()

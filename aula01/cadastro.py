
"""A01 — prática 2. Esqueleto funcional de janela, sem validação pronta."""
import tkinter as tk
from tkinter import ttk


def conferir_cadastro():
    # Obter os textos digitados nos campos
    nome = entrada_nome.get().strip()
    idade_texto = entrada_idade.get().strip()

    # Validar o nome
    if not nome:
        resultado.configure(text="Erro: informe um nome.")
        return

    # Converter e validar a idade
    try:
        idade = int(idade_texto)
    except ValueError:
        resultado.configure(text="Erro: a idade deve ser um número inteiro.")
        return

    if idade <= 0:
        resultado.configure(text="Erro: a idade deve ser maior que zero.")
        return

    # Mostrar o resultado na janela
    resultado.configure(
        text=f"Cadastro conferido nesta sessão!\nNome: {nome}\nIdade: {idade}"
    )


janela = tk.Tk()
janela.title("Conferir cadastro fictício")
janela.columnconfigure(1, weight=1)

ttk.Label(janela, text="Nome fictício:").grid(
    row=0, column=0, padx=12, pady=8, sticky="w"
)
entrada_nome = ttk.Entry(janela)
entrada_nome.grid(row=0, column=1, padx=12, pady=8, sticky="ew")

ttk.Label(janela, text="Idade fictícia:").grid(
    row=1, column=0, padx=12, pady=8, sticky="w"
)
entrada_idade = ttk.Entry(janela)
entrada_idade.grid(row=1, column=1, padx=12, pady=8, sticky="ew")

ttk.Button(
    janela,
    text="Conferir cadastro",
    command=conferir_cadastro
).grid(row=2, column=0, columnspan=2, pady=8)

resultado = ttk.Label(
    janela,
    text="Nenhum cadastro conferido nesta sessão.",
    wraplength=360
)
resultado.grid(
    row=3, column=0, columnspan=2, padx=12, pady=8, sticky="w"
)

entrada_nome.focus_set()
janela.mainloop()

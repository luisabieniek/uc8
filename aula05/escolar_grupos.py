"""A05 — complete: Escolar em grupos — A05."""
import tkinter as tk
from tkinter import ttk
from math import isfinite


def calcular(campos, registro):
    nome = campos["nome"].strip()
    turma = campos["turma"].strip()
    textos_notas = campos["notas"]

    if not nome:
        return "Informe o nome."

    if not turma:
        return "Informe a turma."

    if len(textos_notas) != 5:
        return "Informe exatamente cinco notas."

    notas = []

    for texto in textos_notas:
        try:
            nota = float(texto.strip().replace(",", "."))
        except ValueError:
            return "Todas as notas devem ser números válidos."

        if not isfinite(nota):
            return "As notas devem ser números finitos."

        if nota < 0 or nota > 10:
            return "As notas devem estar entre 0 e 10."

        notas.append(nota)

    media = sum(notas) / len(notas)
    

    registro.update({
        "nome": nome,
        "turma": turma,
        "notas": notas,
        "media": media
    })

    return "Média calculada e registro confirmado."

def exibir(registro):
    if not registro:
        return "Nenhum registro confirmado nesta sessão."
    
    return (
        f"Aluno: {registro['nome']}\n"
        f"Turma: {registro['turma']}\n"
        f"Notas: {', '.join(f'{nota:.1f}' for nota in registro['notas'])}\n"
        f"Média: {registro['media']:.1f}"
    )

def limpar(campos):
    pass


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar em grupos — A05")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = {}
    ttk.Label(base, text="Sistema escolar fictício — organize os campos").grid(row=0, column=0, columnspan=2, pady=6, sticky="w")
    # TODO: criar LabelFrame para identificação e notas e Frame para ações.
    # TODO: posicionar os grupos na base e configurar expansão das colunas.
    # A disposição inicial é plana; substitua os pais e ajuste as linhas internas.
    identificacao = base
    grupo_notas = base
    acoes = base
    base.columnconfigure(1, weight=1)

    ttk.Label(identificacao, text="Nome fictício:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(row=1, column=1, padx=6, pady=4, sticky="ew")
    ttk.Label(identificacao, text="Turma fictícia:").grid(row=2, column=0, padx=6, pady=4, sticky="w")
    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(row=2, column=1, padx=6, pady=4, sticky="ew")
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(grupo_notas, text=f"Nota {numero} (0 a 10):").grid(row=numero+2, column=0, padx=6, pady=4, sticky="w")
        entrada = ttk.Entry(grupo_notas)
        entrada.grid(row=numero+2, column=1, padx=6, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
        campos["nome"] = entrada_nome.get()
        campos["turma"] = entrada_turma.get()
        campos["notas"] = [entrada.get() for entrada in entradas_notas]

        mensagem = calcular(campos, registro)

        aviso.configure(text=mensagem)

    def ao_exibir():
        resultado.configure(text=exibir(registro))

    def ao_limpar():
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)
        for entrada in entradas_notas:
            entrada.delete(0, tk.END)
        aviso.configure(text="Campos limpos.")

    ttk.Button(acoes, text="Calcular média", command=ao_calcular).grid(row=8, column=0, padx=4, pady=6)
    ttk.Button(acoes, text="Exibir", command=ao_exibir).grid(row=8, column=1, padx=4, pady=6)
    ttk.Button(acoes, text="Limpar campos", command=ao_limpar).grid(row=9, column=0, columnspan=2, padx=4, pady=6)
    aviso = ttk.Label(base, text="Use dados fictícios e confira as cinco notas.", wraplength=430)
    aviso.grid(row=10, column=0, columnspan=2, pady=6, sticky="w")
    resultado = ttk.Label(base, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=430)
    resultado.grid(row=11, column=0, columnspan=2, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

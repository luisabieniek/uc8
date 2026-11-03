"""A04 — complete a lógica e os callbacks do sistema escolar."""
import tkinter as tk
from tkinter import ttk


def calcular(campos, registro):
    nome = campos["nome"].strip()
    turma = campos["turma"].strip()
    
    if not nome or not turma:
        return "Erro: nome e turma são obrigatórios."
        
    if len(campos["notas"]) != 5:
        return "Erro: informe exatamente cinco notas."
        
    notas = []
         
    for texto in campos["notas"]:
        try:
             nota = float(texto.strip().replace(",","."))
        except ValueError:
            return "Erro: todas as notas devem ser numéricas."
    
        if nota < 0 or nota > 10:
            return "Erro: as notas devem estar entre 0 e 10."
    
        notas.append(nota)
            
    media = sum(notas) / len(notas)
    
    registro["nome"] = nome
    registro["turma"] = turma
    registro["notas"] = notas
    registro["media"] = media
    
    return "Cálculo realizado com sucesso."


def exibir(registro):
    if not registro:
            return "Nenhum cálculo foi realizado."
    
    return (
        f"Aluno: {registro['nome']}\n"
        f"Turma: {registro['turma']}\n"
        f"Notas: {registro['notas']}\n"
        f"Média: {registro['media']:.1f}"
    )
    


def limpar(campos):
    pass


def criar_janela():
    janela = tk.Tk()
    janela.title("Sistema escolar fictício — A04")
    janela.columnconfigure(1, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = {}

    ttk.Label(janela, text="Dados fictícios. Cinco notas de 0 a 10; média simples.", wraplength=440).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    ttk.Label(janela, text="Nome fictício:").grid(row=1, column=0, padx=12, pady=4, sticky="w")
    entrada_nome = ttk.Entry(janela)
    entrada_nome.grid(row=1, column=1, padx=12, pady=4, sticky="ew")
    ttk.Label(janela, text="Turma fictícia:").grid(row=2, column=0, padx=12, pady=4, sticky="w")
    entrada_turma = ttk.Entry(janela)
    entrada_turma.grid(row=2, column=1, padx=12, pady=4, sticky="ew")
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(janela, text=f"Nota {numero} (0 a 10):").grid(row=numero+2, column=0, padx=12, pady=4, sticky="w")
        entrada = ttk.Entry(janela)
        entrada.grid(row=numero+2, column=1, padx=12, pady=4, sticky="ew")
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
        aviso.configure(text="Campos limpos.")

    ttk.Button(janela, text="Calcular média", command=ao_calcular).grid(row=8, column=0, padx=12, pady=6)
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(row=8, column=1, padx=12, pady=6)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=9, column=0, columnspan=2, pady=4)
    aviso = ttk.Label(janela, text="Preencha nome, turma e as cinco notas fictícias.", wraplength=440)
    aviso.grid(row=10, column=0, columnspan=2, padx=12, pady=6, sticky="w")
    resultado = ttk.Label(janela, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=440)
    resultado.grid(row=11, column=0, columnspan=2, padx=12, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

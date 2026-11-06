"""A05 — complete: Escolar com consulta — A05."""
import tkinter as tk
from tkinter import ttk, messagebox
from math import isfinite
from pathlib import Path
from tkinter import PhotoImage


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
    

    registro.append({
        "nome": nome,
        "turma": turma,
        "notas": notas,
        "media": media
    })

    return f"Média calculada com sucesso: {media:.1f}"


def exibir(registros):
    if not registros:
        return "Nenhum registro confirmado nesta sessão."

    texto = ""

    for registro in registros:
        texto += (
            f"Aluno: {registro['nome']}\n"
            f"Turma: {registro['turma']}\n"
            f"Notas: {', '.join(f'{nota:.1f}' for nota in registro['notas'])}\n"
            f"Média: {registro['media']:.1f}\n\n"
        )

    return texto

def limpar(campos):
    pass


def inserir_marca(container, caminho=None):
    caminho = caminho or Path(__file__).parent / "abc.png"

    try:
        imagem = PhotoImage(file=caminho)
        rotulo = ttk.Label(container, image=imagem)
        rotulo.image = imagem 
        return rotulo   
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return ttk.Label(container, text="Sistema escolar fictício — A05")
    


def abrir_consulta(principal, registro):
    if not registro:
        messagebox.showinfo("Consulta escolar", "Nenhum registro confirmado nesta sessão.")

        return None
    
    texto_confirmado = exibir(registro)

    consulta = tk.Toplevel(principal)
    consulta.title("Consulta escolar — A05")
    
    tk.Label(consulta, text=texto_confirmado, justify="left", padx=10, pady=10).pack(fill="both", expand=True)
    tk.Button(consulta, text="Fechar", command=consulta.destroy).pack(pady=10)

    consulta.lift()
    consulta.focus_force()
    consulta.focus_set()
    consulta.bind("<Escape>", lambda event: consulta.destroy())
    consulta.protocol("WM_DELETE_WINDOW", consulta.destroy)
    consulta.transient(principal)
    consulta.grab_set()
        
    return consulta


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar com consulta — A05")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = []
    inserir_marca(base).grid(row=0, column=0, columnspan=2, pady=6, sticky="w")

    identificacao = ttk.LabelFrame(base, text="Identificação", padding=10)
    grupo_notas = ttk.LabelFrame(base, text="Notas do Aluno", padding=10)
    acoes = ttk.Frame(base, padding=5)
    
    identificacao.grid(row=1, column=0, sticky="nsew", pady=4)
    grupo_notas.grid(row=2, column=0, sticky="nsew", pady=4)
    acoes.grid(row=3, column=0, sticky="ew", pady=6)
    
    identificacao.columnconfigure(1, weight=1)
    grupo_notas.columnconfigure(1, weight=1)
    acoes.columnconfigure((0, 1), weight=1)

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
        abrir_consulta(janela, registro)

    def ao_limpar():
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)

        for entrada in entradas_notas:
            entrada.delete(0, tk.END)

        aviso.configure(text="Campos limpos.")

    ttk.Button(acoes, text="Calcular média", command=ao_calcular).grid(row=8, column=0, padx=4, pady=6)
    ttk.Button(acoes, text="Consultar", command=ao_exibir).grid(row=8, column=1, padx=4, pady=6)
    ttk.Button(acoes, text="Limpar campos", command=ao_limpar).grid(row=9, column=0, columnspan=2, padx=4, pady=6)
    aviso = ttk.Label(base, text="Use dados fictícios e confira as cinco notas.", wraplength=430)
    aviso.grid(row=10, column=0, columnspan=2, pady=6, sticky="w")
    resultado = ttk.Label(base, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=430)
    resultado.grid(row=11, column=0, columnspan=2, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

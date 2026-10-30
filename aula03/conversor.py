"""A03 — complete a lógica e os callbacks do conversor."""
import tkinter as tk
from tkinter import ttk


def calcular(campos, registro):
    try:
        reais = float(campos["reais"].replace(",", "."))
        cotacao_dolar = float(campos["cotacao_dolar"].replace(",", "."))
        cotacao_euro = float(campos["cotacao_euro"].replace(",", "."))
    except ValueError:
        return "Erro: entradas inválidas. Use apenas números."
    
    if reais < 0:
        return "Erro: valor em reais não pode ser negativo."
    
    if cotacao_dolar <= 0 or cotacao_euro <= 0:
        return "Erro: cotações devem ser maiores que zero."
    
    dolares = reais / cotacao_dolar
    euros = reais / cotacao_euro

    registro.update({
        "reais": reais,
        "cotacao_dolar": cotacao_dolar,
        "cotacao_euro": cotacao_euro,
        "dolares": dolares,
        "euros": euros
    })
    return "Conversao realizada."


def exibir(registro):
    if not registro:
        return "Nenhuma conversão confirmada."
    return registro


def limpar(campos):
    pass


def criar_janela():
    janela = tk.Tk()
    janela.title("Conversor com cotações fictícias — A03")
    janela.columnconfigure(1, weight=1)
    campos = {"reais": "", "cotacao_dolar": "", "cotacao_euro": ""}
    registro = {}

    ttk.Label(janela, text="Cotações fictícias manuais; sem consulta à internet.", wraplength=420).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    ttk.Label(janela, text="Valor em reais (R$):").grid(row=1, column=0, padx=12, pady=6, sticky="w")
    entrada_reais = ttk.Entry(janela)
    entrada_reais.grid(row=1, column=1, padx=12, pady=6, sticky="ew")
    ttk.Label(janela, text="R$ por 1 USD:").grid(row=2, column=0, padx=12, pady=6, sticky="w")
    entrada_dolar = ttk.Entry(janela)
    entrada_dolar.grid(row=2, column=1, padx=12, pady=6, sticky="ew")
    ttk.Label(janela, text="R$ por 1 EUR:").grid(row=3, column=0, padx=12, pady=6, sticky="w")
    entrada_euro = ttk.Entry(janela)
    entrada_euro.grid(row=3, column=1, padx=12, pady=6, sticky="ew")

    def ao_calcular():
        campos["reais"] = entrada_reais.get()
        campos["cotacao_dolar"] = entrada_dolar.get()
        campos["cotacao_euro"] = entrada_euro.get()

        mensagem = calcular(campos, registro)
        aviso.configure(text=mensagem)

        resultado.configure(text=exibir(registro))

    def ao_exibir():
        resultado.configure(text=exibir(registro))
        # TODO: consultar somente registro, sem ler as entradas editáveis.
        aviso.configure(text="Consulta ao registro confirmada.")

    def ao_limpar():

        entrada_reais.delete(0, tk.END)
        entrada_dolar.delete(0, tk.END)
        entrada_euro.delete(0, tk.END)

        # TODO: esvaziar campos/Entry e devolver foco; conservar resultado.
        aviso.configure(text="campos limpos")


    ttk.Button(janela, text="Calcular", command=ao_calcular).grid(row=4, column=0, padx=12, pady=8)
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(row=4, column=1, padx=12, pady=8)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=5, column=0, columnspan=2, pady=6)
    aviso = ttk.Label(janela, text="Use vírgula ou ponto decimal, sem milhares.", wraplength=420)
    aviso.grid(row=6, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    resultado = ttk.Label(janela, text="Nenhuma conversão confirmada nesta sessão.", wraplength=420)
    resultado.grid(row=7, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    entrada_reais.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

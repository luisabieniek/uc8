import tkinter as tk
from tkinter import ttk
from pathlib import Path
from aluno import Aluno
from tkinter import PhotoImage
from tkinter import ttk, messagebox


def inserir_marca(container, caminho=None):
    # TODO: procurar marca-a06.png ao lado do script com pathlib.
    # TODO: usar PhotoImage e conservar uma referência enquanto o rótulo existir.
    # TODO: manter texto se o PNG não existir ou não puder ser lido.
    caminho = caminho or Path(__file__).parent / "abcd.png"

    try:
        imagem = PhotoImage(file=caminho)
        rotulo = ttk.Label(container, image=imagem)
        rotulo.image = imagem 
        return rotulo   
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return ttk.Label(container, text="Sistema escolar fictício — A06")


def abrir_consulta(principal, aluno):
    # TODO: tratar ausência de registro sem criar uma janela vazia.
    # TODO: obter o texto do confirmado no instante da abertura.
    # TODO: criar Toplevel e organizar sua consulta somente de leitura.
    # TODO: botão, X e Escape devem fechar somente a consulta.
    if not aluno.notas:
        messagebox.showinfo("Consulta escolar", "Nenhum registro confirmado nesta sessão.",
                            parent=principal)

        return None
    
    texto_confirmado = aluno.resumo()

    consulta = tk.Toplevel(principal)
    consulta.title("Consulta escolar — A06")
    
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
    janela.title("Escolar com consulta — A06")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    aluno = Aluno()  # Uma instância por janela principal, fora dos callbacks.
    inserir_marca(base).grid(row=0, column=0, columnspan=2, pady=6, sticky="w")
    # TODO: criar LabelFrame para identificação e notas e Frame para ações.
    # TODO: posicionar os grupos na base e configurar expansão das colunas.
    # A disposição inicial é plana; substitua os pais e ajuste as linhas internas.

    identificacao = ttk.LabelFrame(
        base, text="Identificação", padding=10
    )
    grupo_notas = ttk.LabelFrame(
        base, text="Notas do Aluno", padding=10
    )
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
        # TODO: ler os sete campos e chamar aluno.atualizar com os textos.
        # TODO: mostrar a mensagem e aluno.resumo; nunca escrever atributos aqui.
        nome = entrada_nome.get()
        turma = entrada_turma.get()
        notas = [entrada.get() for entrada in entradas_notas]

        mensagem = aluno.atualizar(nome, turma, notas)

        aviso.configure(text=mensagem)

        if mensagem == "Aluno atualizado com sucesso.":
            resultado.configure(text=aluno.resumo())
        aviso.configure(text="Integração com o modelo ainda não implementada.")

    def ao_exibir():
        # TODO: adaptar sua consulta da A05 para receber aluno.
        abrir_consulta(janela, aluno)

    def ao_limpar():
        # TODO: limpar só os campos e devolver foco, preservando aluno e consultas.
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

import tkinter as tk
from tkinter import ttk


def comparar():
    try:
        import customtkinter as ctk
    except ImportError:
        return "CustomTkinter não instalado. A interface ttk continua funcionando."
    return "ttk e CustomTkinter disponíveis para comparação visual."


if __name__ == "__main__":
    print(comparar())

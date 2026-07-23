import tkinter as tk
from tkinter import messagebox
import sql_cad_Cta_Agr as sql

def tela_cadctaagr():


    def atualizar_lista():
        listbox.delete(0, tk.END)
        for r in sql.listar():
            listbox.insert(tk.END, r)

    def inserir():
        sql.inserir(entry_nome.get(), entry_desc.get())
        atualizar_lista()
        messagebox.showinfo("OK", "Grupo inserido.")

    def atualizar():
        sql.atualizar(int(entry_cod.get()), entry_nome.get(), entry_desc.get())
        atualizar_lista()
        messagebox.showinfo("OK", "Grupo atualizado.")

    def excluir():
        sql.excluir(int(entry_cod.get()))
        atualizar_lista()
        messagebox.showinfo("OK", "Grupo excluído.")

    janela = tk.Toplevel()
    janela.title("Cadastro de Grupos de Contas")
    janela.geometry("500x500")

    tk.Label(janela, text="Código").pack()
    entry_cod = tk.Entry(janela)
    entry_cod.pack()

    tk.Label(janela, text="Nome do Grupo").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Descrição").pack()
    entry_desc = tk.Entry(janela)
    entry_desc.pack()

    tk.Button(janela, text="Inserir", command=inserir).pack(pady=5)
    tk.Button(janela, text="Atualizar", command=atualizar).pack(pady=5)
    tk.Button(janela, text="Excluir", command=excluir).pack(pady=5)

    listbox = tk.Listbox(janela, width=60, height=15)
    listbox.pack(pady=10)

    atualizar_lista()

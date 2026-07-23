import tkinter as tk
from tkinter import messagebox, ttk
import sql.sql_cadctaagr as sql
from datetime import datetime

def tela_cadctaagr():

    janela = tk.Toplevel()
    janela.title("Cadastro de Grupos de Contas")
    janela.geometry("600x600")
    janela.grab_set()
    janela.focus_force()

    def somente_numeros(P):
        return P.isdigit() or P == ""

    def limitar_5(P):
        return len(P) <= 5

    def limitar_50(P):
        return len(P) <= 50

    validar_num = janela.register(somente_numeros)
    validar_5 = janela.register(limitar_5)
    validar_50 = janela.register(limitar_50)

    registro_original = {"CODCTAAGR": None}

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)

        for r in sql.listar():
            tree.insert("", tk.END, values=(r[0], r[1], r[2]))

    def preencher_campos(event):
        item = tree.selection()
        if item:
            valores = tree.item(item, "values")

            entry_cod.delete(0, tk.END)
            entry_cod.insert(0, valores[0])

            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, valores[1])

            entry_dta.delete(0, tk.END)
            entry_dta.insert(0, valores[2])

            registro_original["CODCTAAGR"] = valores[0]

    def inserir():
        if not messagebox.askyesno("Confirmação", "Deseja inserir este grupo?"):
            return

        cod = entry_cod.get()
        desc = entry_desc.get()
        dta = entry_dta.get()

        if not cod or not desc or not dta:
            messagebox.showwarning("Campos", "Preencha todos os campos.")
            return

        if sql.existe(cod):
            messagebox.showwarning("Duplicado", "Já existe um grupo com este código.")
            return

        sql.inserir(cod, desc, dta)
        atualizar_lista()
        messagebox.showinfo("OK", "Grupo inserido.")

    def atualizar():
        if not messagebox.askyesno("Confirmação", "Deseja atualizar este grupo?"):
            return

        cod_original = registro_original["CODCTAAGR"]

        if cod_original is None:
            messagebox.showwarning("Erro", "Selecione um grupo antes de atualizar.")
            return

        if not sql.existe(cod_original):
            messagebox.showerror("Inexistente", "O grupo original não existe mais.")
            return

        cod_novo = entry_cod.get()
        desc = entry_desc.get()
        dta = entry_dta.get()

        if cod_novo != cod_original and sql.existe(cod_novo):
            messagebox.showwarning("Duplicado", "Já existe um grupo com este novo código.")
            return

        sql.excluir(cod_original)
        sql.inserir(cod_novo, desc, dta)

        atualizar_lista()
        messagebox.showinfo("OK", "Grupo atualizado.")

        registro_original["CODCTAAGR"] = None

    def excluir():
        if not messagebox.askyesno("Confirmação", "Deseja excluir este grupo?"):
            return

        cod = entry_cod.get()

        if not sql.existe(cod):
            messagebox.showerror("Inexistente", "Este grupo não existe.")
            return

        sql.excluir(cod)
        atualizar_lista()
        messagebox.showinfo("OK", "Grupo excluído.")

    tk.Label(janela, text="Código do Grupo").pack()
    entry_cod = tk.Entry(janela, validate="key",
                         validatecommand=(validar_num, "%P"))
    entry_cod.pack()
    entry_cod.config(validatecommand=(validar_5, "%P"))

    tk.Label(janela, text="Descrição do Grupo").pack()
    entry_desc = tk.Entry(janela, validate="key",
                          validatecommand=(validar_50, "%P"))
    entry_desc.pack()

    tk.Label(janela, text="Data de Abertura (dd/mm/aaaa)").pack()
    entry_dta = tk.Entry(janela)
    entry_dta.pack()
    entry_dta.insert(0, datetime.now().strftime("%d/%m/%Y"))

    frame_tree = tk.Frame(janela)
    frame_tree.pack(pady=10)

    colunas = ("CODCTAAGR", "DESCRCTAAGR", "DTAABERTURA")
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=15)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    tree.bind("<<TreeviewSelect>>", preencher_campos)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Inserir", command=inserir).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", command=excluir).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Finalizar", command=janela.destroy).pack(side="left", padx=5)

    atualizar_lista()

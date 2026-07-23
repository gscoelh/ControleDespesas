import tkinter as tk
from tkinter import messagebox, ttk
import sql.sql_roteirocapa as sql
import sql.sql_cadconta as sql_conta
import sql.sql_tipolote as sql_lote

def tela_roteirocapa():

    janela = tk.Toplevel()
    janela.title("Cadastro de Roteiro - Capa")
    janela.geometry("700x700")
    janela.grab_set()
    janela.focus_force()

    def limitar_5(P):
        return len(P) <= 5

    def limitar_50(P):
        return len(P) <= 50

    validar_5 = janela.register(limitar_5)
    validar_50 = janela.register(limitar_50)

    registro_original = {"ROTEIRO": None}

    def carregar_combos():
        contas = sql_conta.listar()
        combo_conta['values'] = [f"{c[0]} - {c[1]}" for c in contas]

        lotes = sql_lote.listar()
        combo_lote['values'] = [f"{l[0]} - {l[1]}" for l in lotes]

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)
        for r in sql.listar():
            tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4]))

    def preencher_campos(event):
        item = tree.selection()
        if item:
            valores = tree.item(item, "values")

            entry_rot.delete(0, tk.END)
            entry_rot.insert(0, valores[0])

            var_nat.set(valores[1])

            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, valores[2])

            combo_conta.set(valores[3])
            combo_lote.set(valores[4])

            registro_original["ROTEIRO"] = valores[0]
            btn_atualizar.config(state="normal")
            btn_excluir.config(state="normal")

    def bloquear_botoes(event=None):
        btn_atualizar.config(state="disabled")
        btn_excluir.config(state="disabled")

    def inserir():
        rot = entry_rot.get()
        nat = var_nat.get()
        desc = entry_desc.get()
        conta = combo_conta.get().split(" - ")[0]
        lote = combo_lote.get().split(" - ")[0]

        if not rot or not nat or not desc or not conta or not lote:
            messagebox.showwarning("Campos", "Preencha todos os campos.")
            return

        if sql.existe(rot):
            messagebox.showwarning("Duplicado", "Já existe este roteiro.")
            return

        sql.inserir(rot, nat, desc, conta, lote)
        atualizar_lista()
        messagebox.showinfo("OK", "Registro inserido.")

    def atualizar():
        rot_original = registro_original["ROTEIRO"]
        if rot_original is None:
            messagebox.showwarning("Erro", "Selecione um registro.")
            return

        rot_novo = entry_rot.get()
        nat = var_nat.get()
        desc = entry_desc.get()
        conta = combo_conta.get().split(" - ")[0]
        lote = combo_lote.get().split(" - ")[0]

        if rot_novo != rot_original and sql.existe(rot_novo):
            messagebox.showwarning("Duplicado", "Já existe este novo código.")
            return

        sql.excluir(rot_original)
        sql.inserir(rot_novo, nat, desc, conta, lote)

        atualizar_lista()
        messagebox.showinfo("OK", "Registro atualizado.")
        registro_original["ROTEIRO"] = None

    def excluir():
        rot = entry_rot.get()
        if not sql.existe(rot):
            messagebox.showerror("Inexistente", "Este registro não existe.")
            return
        sql.excluir(rot)
        atualizar_lista()
        messagebox.showinfo("OK", "Registro excluído.")

    tk.Label(janela, text="Código do Roteiro").pack()
    entry_rot = tk.Entry(janela, validate="key", validatecommand=(validar_5, "%P"))
    entry_rot.pack()
    entry_rot.bind("<KeyRelease>", bloquear_botoes)

    tk.Label(janela, text="Natureza").pack()
    var_nat = tk.StringVar(value="D")
    frame_nat = tk.Frame(janela)
    frame_nat.pack()
    tk.Radiobutton(frame_nat, text="Débito (D)", variable=var_nat, value="D").pack(side="left", padx=5)
    tk.Radiobutton(frame_nat, text="Crédito (C)", variable=var_nat, value="C").pack(side="left", padx=5)

    tk.Label(janela, text="Descrição").pack()
    entry_desc = tk.Entry(janela, validate="key", validatecommand=(validar_50, "%P"))
    entry_desc.pack()

    tk.Label(janela, text="Conta da Natureza").pack()
    combo_conta = ttk.Combobox(janela, width=50)
    combo_conta.pack()
    combo_conta.bind("<<ComboboxSelected>>", bloquear_botoes)

    tk.Label(janela, text="Título do Lote").pack()
    combo_lote = ttk.Combobox(janela, width=50)
    combo_lote.pack()
    combo_lote.bind("<<ComboboxSelected>>", bloquear_botoes)

    frame_tree = tk.Frame(janela)
    frame_tree.pack(pady=10)

    colunas = ("ROTEIRO", "ROTNATUREZA", "ROTDESC", "CONTADANATUREZA", "TITULOLOTE")
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
    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar)
    btn_atualizar.pack(side="left", padx=5)
    btn_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir)
    btn_excluir.pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Finalizar", command=janela.destroy).pack(side="left", padx=5)

    btn_atualizar.config(state="disabled")
    btn_excluir.config(state="disabled")

    carregar_combos()
    atualizar_lista()

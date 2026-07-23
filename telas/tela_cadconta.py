import tkinter as tk
from tkinter import messagebox, ttk
import sql.sql_cadconta as sql
from datetime import datetime

def tela_cadconta():

    janela = tk.Toplevel()
    janela.title("Cadastro de Contas")
    janela.geometry("700x700")
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

    registro_original = {"CODCTA": None}

    def carregar_comboboxes():
        grupos = sql.listar_grupos()
        combo_ctaagr['values'] = [f"{g[0]} - {g[1]}" for g in grupos]

        custos = sql.listar_tipos_custo()
        combo_tpcusto['values'] = [c[0] for c in custos]

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)

        for r in sql.listar():
            tree.insert("", tk.END, values=(r[0], r[1], r[2], r[4], r[5], r[6]))

    def preencher_campos(event):
        item = tree.selection()
        if item:
            valores = tree.item(item, "values")

            entry_cod.delete(0, tk.END)
            entry_cod.insert(0, valores[0])

            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, valores[1])

            combo_ctaagr.set(valores[2])
            combo_tpcusto.set(valores[3])

            if valores[4] == "D":
                var_natureza.set("D")
            else:
                var_natureza.set("C")

            entry_dtaabert.delete(0, tk.END)
            entry_dtaabert.insert(0, valores[5])

            registro_original["CODCTA"] = valores[0]

    def inserir():
        if not messagebox.askyesno("Confirmação", "Deseja inserir esta conta?"):
            return

        cod = entry_cod.get()
        desc = entry_desc.get()
        agr = combo_ctaagr.get().split(" - ")[0]
        custo = combo_tpcusto.get()
        natureza = var_natureza.get()
        dtaabert = entry_dtaabert.get()

        if not cod or not desc or not agr or not custo or not natureza or not dtaabert:
            messagebox.showwarning("Campos", "Preencha todos os campos.")
            return

        if sql.existe(cod):
            messagebox.showwarning("Duplicado", "Já existe uma conta com este código.")
            return

        sql.inserir(cod, desc, agr, custo, natureza, dtaabert)
        atualizar_lista()
        messagebox.showinfo("OK", "Conta inserida.")

    def atualizar():
        if not messagebox.askyesno("Confirmação", "Deseja atualizar esta conta?"):
            return

        cod_original = registro_original["CODCTA"]

        if cod_original is None:
            messagebox.showwarning("Erro", "Selecione uma conta antes de atualizar.")
            return

        if not sql.existe(cod_original):
            messagebox.showerror("Inexistente", "A conta original não existe mais.")
            return

        cod_novo = entry_cod.get()
        desc = entry_desc.get()
        agr = combo_ctaagr.get().split(" - ")[0]
        custo = combo_tpcusto.get()
        natureza = var_natureza.get()
        dtaabert = entry_dtaabert.get()

        if cod_novo != cod_original and sql.existe(cod_novo):
            messagebox.showwarning("Duplicado", "Já existe uma conta com este novo código.")
            return

        sql.excluir(cod_original)
        sql.inserir(cod_novo, desc, agr, custo, natureza, dtaabert)

        atualizar_lista()
        messagebox.showinfo("OK", "Conta atualizada.")

        registro_original["CODCTA"] = None

    def excluir():
        if not messagebox.askyesno("Confirmação", "Deseja excluir esta conta?"):
            return

        cod = entry_cod.get()

        if not sql.existe(cod):
            messagebox.showerror("Inexistente", "Esta conta não existe.")
            return

        sql.excluir(cod)
        atualizar_lista()
        messagebox.showinfo("OK", "Conta excluída.")

    tk.Label(janela, text="Código da Conta").pack()
    entry_cod = tk.Entry(janela, validate="key",
                         validatecommand=(validar_num, "%P"))
    entry_cod.pack()
    entry_cod.config(validatecommand=(validar_5, "%P"))

    tk.Label(janela, text="Descrição da Conta").pack()
    entry_desc = tk.Entry(janela, validate="key",
                          validatecommand=(validar_50, "%P"))
    entry_desc.pack()

    tk.Label(janela, text="Conta Aglutinadora (CADCTAAGR)").pack()
    combo_ctaagr = ttk.Combobox(janela, width=50)
    combo_ctaagr.pack()

    tk.Label(janela, text="Tipo de Custo (CONTASPORCUSTO)").pack()
    combo_tpcusto = ttk.Combobox(janela, width=50)
    combo_tpcusto.pack()

    tk.Label(janela, text="Natureza da Conta").pack()
    var_natureza = tk.StringVar(value="D")
    frame_nat = tk.Frame(janela)
    frame_nat.pack()
    tk.Radiobutton(frame_nat, text="Débito (D)", variable=var_natureza, value="D").pack(side="left", padx=5)
    tk.Radiobutton(frame_nat, text="Crédito (C)", variable=var_natureza, value="C").pack(side="left", padx=5)

    tk.Label(janela, text="Data de Abertura (dd/mm/aaaa)").pack()
    entry_dtaabert = tk.Entry(janela)
    entry_dtaabert.pack()
    entry_dtaabert.insert(0, datetime.now().strftime("%d/%m/%Y"))

    frame_tree = tk.Frame(janela)
    frame_tree.pack(pady=10)

    colunas = ("CODCTA", "DESCRCTA", "CODCTAAGR", "TPCUSTO", "NATUREZA", "DTAABERT")
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=15)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)

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

    carregar_comboboxes()
    atualizar_lista()

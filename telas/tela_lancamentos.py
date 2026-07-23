import tkinter as tk
from tkinter import ttk, messagebox
import os

import sql.sql_roteirocapa as sql_capa
import sql.sql_roteirodeta as sql_deta
import sql.sql_lancamentos as sql_lanc
import sql.sql_cadconta as sql_conta

from core import config

PASTA_COMPROVANTES = config.get_pasta_comprovantes()
AUTOCOMP = set(config.get_complementos())


def tela_lancamentos():

    janela = tk.Toplevel()
    janela.title("Lançamentos Diários")
    janela.geometry("1200x800")
    janela.grab_set()

    ultimo_comprovante = {"nome": ""}

    # ===========================
    # CABEÇALHO
    # ===========================
    frame_top = tk.Frame(janela)
    frame_top.pack(fill="x", pady=10)

    tk.Label(frame_top, text="Roteiro").pack(side="left", padx=5)
    combo_roteiro = ttk.Combobox(frame_top, width=50)
    combo_roteiro.pack(side="left", padx=5)

    roteiros = sql_capa.listar()
    combo_roteiro["values"] = [f"{r[0]} - {r[2]}" for r in roteiros]

    tk.Label(frame_top, text="Competência (MMAAAA)").pack(side="left", padx=5)
    entry_comp = tk.Entry(frame_top, width=10)
    entry_comp.pack(side="left", padx=5)

    btn_carregar = tk.Button(frame_top, text="Carregar")
    btn_carregar.pack(side="left", padx=10)

    # ===========================
    # VALIDAR COMPETÊNCIA
    # ===========================
    def validar_competencia(event):
        comp = entry_comp.get().strip()

        if len(comp) > 6:
            entry_comp.delete(6, tk.END)
            return

        if not comp.isdigit():
            entry_comp.delete(0, tk.END)
            return

        if len(comp) == 6:
            mes = int(comp[:2])
            ano = int(comp[2:])

            if mes < 1 or mes > 12:
                messagebox.showwarning("Competência inválida", "Mês deve estar entre 01 e 12.")
                entry_comp.delete(0, tk.END)
                return

            if ano < 2000 or ano > 2099:
                messagebox.showwarning("Competência inválida", "Ano deve estar entre 2000 e 2099.")
                entry_comp.delete(0, tk.END)
                return

            carregar()

    entry_comp.bind("<KeyRelease>", validar_competencia)

    # ===========================
    # SPREAD
    # ===========================
    frame_tree = tk.Frame(janela)
    frame_tree.pack(pady=10)

    colunas = ("DIA", "CONTA", "HISTORICO", "COMPLHISTORICO", "VALOR",
               "COMPROVANTE", "COMPPATH", "DATAFULL")
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=18)

    tree.column("COMPPATH", width=0, stretch=False)
    tree.column("DATAFULL", width=0, stretch=False)

    ordem_atual = {col: False for col in colunas}

    def ordenar_por_coluna(col):
        itens = [(tree.set(iid, col), iid) for iid in tree.get_children("")]

        if col == "VALOR":
            def chave(x):
                try:
                    return float(x[0].replace(".", "").replace(",", "."))
                except:
                    return 0.0
        else:
            def chave(x):
                return x[0]

        ordem_atual[col] = not ordem_atual[col]
        reverse = ordem_atual[col]

        itens.sort(key=chave, reverse=reverse)

        for index, (_, iid) in enumerate(itens):
            tree.move(iid, "", index)

    for col in colunas[:-2]:
        tree.heading(col, text=col, command=lambda c=col: ordenar_por_coluna(c))
        tree.column(col, width=180)

    tree.pack()

    # ===========================
    # CAMPOS DE EDIÇÃO
    # ===========================
    frame_edit = tk.LabelFrame(janela, text="Edição do Lançamento")
    frame_edit.pack(fill="x", padx=10, pady=10)

    def campo(label):
        linha = tk.Frame(frame_edit)
        linha.pack(fill="x", pady=3)
        tk.Label(linha, text=label, width=20, anchor="w").pack(side="left")
        entry = tk.Entry(linha, width=60)
        entry.pack(side="left")
        return entry

    txt_dia = campo("Dia")
    txt_conta = campo("Conta (fixa)")
    txt_hist = campo("Histórico (fixo)")
    txt_compl = campo("Complemento Histórico")
    txt_valor = campo("Valor")

    linha_comp = tk.Frame(frame_edit)
    linha_comp.pack(fill="x", pady=3)
    tk.Label(linha_comp, text="Comprovante", width=20, anchor="w").pack(side="left")
    combo_comp = ttk.Combobox(linha_comp, width=57)
    combo_comp.pack(side="left")

    txt_conta.config(state="disabled")
    txt_hist.config(state="disabled")

    # ===========================
    # AUTOCOMPLETE INTELIGENTE
    # ===========================
    def autocomplete_compl(event):
        texto = txt_compl.get()
        if not texto:
            return

        possiveis = [s for s in AUTOCOMP if s.lower().startswith(texto.lower())]
        if possiveis:
            sugestao = possiveis[0]
            txt_compl.delete(0, tk.END)
            txt_compl.insert(0, sugestao)
            txt_compl.select_range(len(texto), len(sugestao))

    txt_compl.bind("<KeyRelease>", autocomplete_compl)

    # ===========================
    # LIMPAR CAMPOS
    # ===========================
    def limpar_campos():
        for campo in (txt_dia, txt_conta, txt_hist, txt_compl, txt_valor):
            campo.config(state="normal")
            campo.delete(0, tk.END)
            campo.config(state="disabled")

        combo_comp.set("")
        combo_comp.config(state="disabled")

    limpar_campos()

    # ===========================
    # FORMATAR VALOR
    # ===========================
    def formatar_valor(event):
        valor = txt_valor.get().strip()
        if not valor:
            return

        valor = valor.replace(".", ",")
        if "," in valor:
            partes = valor.split(",")
            if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                centavos = partes[1].ljust(2, "0")[:2]
                txt_valor.delete(0, tk.END)
                txt_valor.insert(0, f"{partes[0]},{centavos}")
                return

        if valor.isdigit():
            if len(valor) == 1:
                txt_valor.delete(0, tk.END)
                txt_valor.insert(0, f"0,0{valor}")
            elif len(valor) == 2:
                txt_valor.delete(0, tk.END)
                txt_valor.insert(0, f"0,{valor}")
            else:
                txt_valor.delete(0, tk.END)
                txt_valor.insert(0, valor[:-2] + "," + valor[-2:])

    txt_valor.bind("<FocusOut>", formatar_valor)

    # ===========================
    # CARREGAR COMPROVANTES
    # ===========================
    def carregar_comprovantes():
        try:
            arquivos = os.listdir(PASTA_COMPROVANTES)
            arquivos = [arq for arq in arquivos
                        if os.path.isfile(os.path.join(PASTA_COMPROVANTES, arq))]
            arquivos.sort()
            combo_comp["values"] = arquivos
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar comprovantes:\n{e}")

    # ===========================
    # CARREGAR LANÇAMENTOS
    # ===========================
    def carregar():
        carregar_comprovantes()

        for item in tree.get_children():
            tree.delete(item)

        comp = entry_comp.get().strip()
        if len(comp) != 6:
            return

        mes = int(comp[:2])
        ano = int(comp[2:])
        rot = combo_roteiro.get().split(" - ")[0]

        conta_capa = sql_capa.buscar_conta(rot)

        linhas = sql_deta.listar()
        for r in linhas:
            if r[0] == rot:
                conta_spread = r[2] if r[1] == "D" else r[3]
                nome = next((c[1] for c in sql_conta.listar() if c[0] == conta_spread), "")
                tree.insert("", tk.END, values=("", conta_spread, nome, "", "", "", "", ""))

        existentes = sql_lanc.listar_por_roteiro_competencia(rot, mes, ano)

        for lan in existentes:
            dia = lan[0].strftime("%d")
            datafull = lan[0].strftime("%Y-%m-%d")
            conta = lan[1]
            hist = lan[2]
            compl = lan[3]
            valor = f"{lan[4]:.2f}".replace(".", ",")
            compweb = lan[7]
            nome_arquivo = os.path.basename(compweb) if compweb else ""

            if conta != conta_capa:
                tree.insert(
                    "",
                    tk.END,
                    values=(dia, conta, hist, compl, valor, nome_arquivo, compweb, datafull)
                )

    btn_carregar.config(command=carregar)

    # ===========================
    # SELECIONAR LINHA
    # ===========================
    def selecionar(event):
        item = tree.selection()
        if not item:
            return

        valores = tree.item(item[0], "values")

        for campo in (txt_dia, txt_compl, txt_valor):
            campo.config(state="normal")

        combo_comp.config(state="normal")

        txt_conta.config(state="normal")
        txt_hist.config(state="normal")

        txt_dia.delete(0, tk.END)
        txt_conta.delete(0, tk.END)
        txt_hist.delete(0, tk.END)
        txt_compl.delete(0, tk.END)
        txt_valor.delete(0, tk.END)

        txt_dia.insert(0, valores[0])
        txt_conta.insert(0, valores[1])
        txt_hist.insert(0, valores[2])
        txt_compl.insert(0, valores[3])
        txt_valor.insert(0, valores[4])

        if ultimo_comprovante["nome"]:
            combo_comp.set(ultimo_comprovante["nome"])
        else:
            combo_comp.set(valores[5])

        txt_conta.config(state="disabled")
        txt_hist.config(state="disabled")

        txt_dia.focus_set()

    tree.bind("<<TreeviewSelect>>", selecionar)

    # ===========================
    # ABRIR COMPROVANTE
    # ===========================
    def abrir_comprovante(event):
        item = tree.selection()
        if not item:
            return

        valores = tree.item(item[0], "values")
        caminho = valores[6]

        if not caminho:
            messagebox.showwarning("Comprovante", "Nenhum comprovante associado.")
            return

        if not os.path.exists(caminho):
            messagebox.showerror("Comprovante", f"Arquivo não encontrado:\n{caminho}")
            return

        try:
            os.system(f'start msedge "{caminho}"')
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o comprovante:\n{e}")

    tree.bind("<Double-1>", abrir_comprovante)

    # ===========================
    # EXCLUIR LANÇAMENTO
    # ===========================
    def excluir_linha():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Excluir", "Selecione uma linha.")
            return

        dia, conta, hist, compl, valor, nome_comp, compweb, datafull = tree.item(item[0], "values")

        if not dia or not valor:
            messagebox.showwarning("Excluir", "Linha vazia não pode ser excluída.")
            return

        sql_lanc.excluir_lancamento_duplo(
            datafull, conta, hist, compl, valor.replace(",", "."), compweb
        )
        tree.delete(item[0])

        limpar_campos()

    # ===========================
    # GRAVAR LANÇAMENTO
    # ===========================
    def gravar_linha():
        try:
            dia = txt_dia.get().strip()
            conta_spread = txt_conta.get().strip()
            hist = txt_hist.get().strip()
            compl = txt_compl.get().strip()
            valor = txt_valor.get().strip()
            arquivo = combo_comp.get().strip()

            if not dia or not valor or not arquivo or not conta_spread:
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return

            comprovante = os.path.join(PASTA_COMPROVANTES, arquivo)

            valor = valor.replace(" ", "").replace(".", ",")
            if "," in valor:
                partes = valor.split(",")
                if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
                    messagebox.showwarning("Valor inválido", "Digite um valor válido, ex: 345,88")
                    return
                centavos = partes[1].ljust(2, "0")[:2]
                valor_decimal = f"{partes[0]},{centavos}"
            else:
                if not valor.isdigit():
                    messagebox.showwarning("Valor inválido", "Digite apenas números ou números com vírgula.")
                    return
                if len(valor) == 1:
                    valor_decimal = f"0,0{valor}"
                elif len(valor) == 2:
                    valor_decimal = f"0,{valor}"
                else:
                    valor_decimal = valor[:-2] + "," + valor[-2:]

            valor_sql = valor_decimal.replace(",", ".")

            comp = entry_comp.get().strip()
            mes = int(comp[:2])
            ano = int(comp[2:])
            datalancto = f"{ano}-{mes}-{dia}"

            rot = combo_roteiro.get().split(" - ")[0]
            conta_capa = sql_capa.buscar_conta(rot)

            titulolote = sql_capa.buscar_titulolote(rot)
            lote = f"{titulolote}{comp}"
            
            seq = sql_lanc.proximo_sequencial_lote(lote)
            quemweb = "Geraldo"

            if compl:
                AUTOCOMP.add(compl)
                config.add_complemento(compl)

            ultimo_comprovante["nome"] = arquivo

            item = tree.selection()
            if item:
                dia_old, conta_old, hist_old, compl_old, valor_old, nome_old, comp_old, data_old = tree.item(item[0], "values")
                if valor_old.strip() != "":
                    sql_lanc.excluir_lancamento_duplo(
                        data_old, conta_old, hist_old, compl_old,
                        valor_old.replace(",", "."), comp_old
                    )

            sql_lanc.inserir(
                datalancto, rot, conta_capa, valor_sql, "D",
                hist, compl, conta_spread, datalancto,
                lote, seq, quemweb, comprovante
            )

            sql_lanc.inserir(
                datalancto, rot, conta_spread, valor_sql, "C",
                hist, compl, conta_capa, datalancto,
                lote, seq, quemweb, comprovante
            )

            if item:
                tree.item(
                    item[0],
                    values=(dia, conta_spread, hist, compl, valor_decimal, arquivo, comprovante, datalancto)
                )
            else:
                tree.insert(
                    "",
                    tk.END,
                    values=(dia, conta_spread, hist, compl, valor_decimal, arquivo, comprovante, datalancto)
                )

            tree.insert("", tk.END, values=("", conta_spread, hist, "", "", "", "", ""))

            limpar_campos()

            messagebox.showinfo("OK", "Lançamento gravado.")

        except Exception as e:
            messagebox.showerror("Erro ao gravar", str(e))

    # ===========================
    # BOTÕES
    # ===========================
    frame_buttons = tk.Frame(janela)
    frame_buttons.pack(fill="x", pady=10)

    tk.Button(frame_buttons, text="Excluir Linha", command=excluir_linha).pack(side="left", padx=10)
    tk.Button(frame_buttons, text="Gravar Linha", command=gravar_linha).pack(side="left", padx=10)
    tk.Button(frame_buttons, text="Finalizar", command=janela.destroy).pack(side="left", padx=10)

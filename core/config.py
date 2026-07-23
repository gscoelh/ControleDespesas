import configparser
import os

# Caminho absoluto do config.ini
INI_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
INI_PATH = os.path.abspath(INI_PATH)

config = configparser.ConfigParser()

# ===========================
# CRIA O INI SE NÃO EXISTIR
# ===========================
if not os.path.exists(INI_PATH):
    config["AMBIENTE"] = {
        "MODO": "DESENV",
        "MOSTRAR_ALERTA": "SIM"
    }

    config["BANCOS"] = {
        "DESENV": r"C:\Users\User\Documents\CONTROLE_DESPESAS\NOVODESPESAS_TESTE.mdb",
        "PRODUC": r"C:\Users\User\Documents\CONTROLE_DESPESAS\NOVODESPESAS_OFICIAL.mdb"
    }

    config["PASTAS"] = {
        "COMPROVANTES": r"C:\Users\User\OneDrive\Documents\ComprovantePagamentos"
    }

    config["AUTOCOMPLETE"] = {
        "PALAVRAS": ""
    }

    with open(INI_PATH, "w") as f:
        config.write(f)

# ===========================
# CARREGA O INI
# ===========================
config.read(INI_PATH)

# ===========================
# AMBIENTE
# ===========================
def get_modo():
    return config["AMBIENTE"]["MODO"]

def get_alerta():
    return config["AMBIENTE"]["MOSTRAR_ALERTA"]

def set_modo(novo):
    config["AMBIENTE"]["MODO"] = novo
    with open(INI_PATH, "w") as f:
        config.write(f)

def set_alerta(valor):
    config["AMBIENTE"]["MOSTRAR_ALERTA"] = valor
    with open(INI_PATH, "w") as f:
        config.write(f)

# ===========================
# BANCO DE DADOS
# ===========================
def get_db_path():
    modo = get_modo()

    if modo == "DESENV":
        return config["BANCOS"]["DESENV"]
    else:
        return config["BANCOS"]["PRODUC"]

# ===========================
# PASTAS
# ===========================
def get_pasta_comprovantes():
    return config["PASTAS"]["COMPROVANTES"]

# ===========================
# AUTOCOMPLETE
# ===========================
def get_complementos():
    palavras = config["AUTOCOMPLETE"]["PALAVRAS"]
    return [p.strip() for p in palavras.split(",") if p.strip()]

def add_complemento(novo):
    palavras = get_complementos()

    if novo not in palavras:
        palavras.append(novo)

        # Limita a 200 palavras
        palavras = palavras[-200:]

        config["AUTOCOMPLETE"]["PALAVRAS"] = ",".join(palavras)

        with open(INI_PATH, "w") as f:
            config.write(f)

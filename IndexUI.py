import streamlit as st
import pandas as pd
from Templates.ManterDados import Dados
from Templates.ManterOperações import Operações
from Templates.ManterMédias import Médias

# from Templates.LoginUI import loginUI
# from Templates.AbrirConta import abrirConta
# from Templates.ManterUsuário import manterUsuário
# from View import View

# Criando um DataFrame do zero
dados = {
    'clientes': [
        "192.168.1.10",
        "192.168.0.25",
        "10.0.0.15",
        "10.1.1.50",
        "172.16.5.100"
    ],  # Dados de clientes
    'temperatura': [23, 24, 22, 21, 23],    # Dados de temperatura
    'Quantidade de processadores': [4, 8, 4, 16, 8],  # Quantidade de processadores
    'Memória Ram Livre (GB)': [8, 16, 4, 32, 8],  # Memória RAM livre em GB
    'Espaço em disco livre (GB)': [500, 1000, 200, 1500, 500],  # Espaço em disco livre
}
# Convertendo para um DataFrame do pandas
df = pd.DataFrame(dados)
#df = df.reset_index(drop=True)

class IndexUI:

    def __init__(self, menu):
        self.__menu = menu

    def main(self):
        self.op = st.sidebar.selectbox("MENU:", self.__menu)

        if self.op == "Dados":
            Dados.main(self.op, df)
        elif self.op == "Médias":
            Médias.main(self.op, df)
        elif self.op == "Operações":
            Operações.main(self.op, df)
        else:
            Dados.main(self.op, df[df["clientes"]== self.op])

menu = ["Dados", "Médias", "Operações"] + df["clientes"].tolist()
    
app = IndexUI(menu)
app.main()
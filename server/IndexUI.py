
import streamlit as st
import pandas as pd
import json
import time
from Templates.ManterDados import Dados
from Templates.ManterOperações import Operações
from Templates.ManterMédias import Médias

class IndexUI:
    @classmethod
    def carregar_dados(cls):
        with open("data.json", "r") as f:
            data = json.load(f)
        
        df = pd.DataFrame([{  
            'Cliente': ip,
            'Hostname': info['hostname'],
            'Sistema Operacional': info['sistema_operacional'],
            'Arquitetura': info['arquitetura'],
            'Processadores': info['processadores'],
            'Frequência CPU (MHz)': info['frequencia_cpu_mhz'],
            'Memória RAM Total (GB)': info['ram_total_gb'],
            'Memória RAM Livre (GB)': info['ram_livre_gb'],
            'Espaço em Disco Total (GB)': info['disco_total_gb'],
            'Espaço em Disco Livre (GB)': info['disco_livre_gb'],
            'Uso CPU (%)': info['uso_cpu_percent'],
            'Uso RAM (%)': info['uso_ram_percent'],
            'Uso Disco (%)': info['uso_disco_percent'],
            'Temperatura CPU': info['temperatura_cpu'],
            'IP Local': info['ip_local'],
            'IP Público': info['ip_publico'],
            'MAC Address': info['mac_address'],
            'Latência Google (ms)': info['latencia_google_ms'],
            'Nível Bateria (%)': info['nivel_bateria'],
            'Carregando': info['carregando']
        } for ip, info in data.items()])  
        
        return df
    
    @classmethod
    def main(cls):
        st.sidebar.title("Menu")

        if "pagina_atual" not in st.session_state:
            st.session_state.pagina_atual = "Dados"

        op = st.sidebar.selectbox("Selecione uma opção:", ["Dados", "Médias", "Operações"], index=["Dados", "Médias", "Operações"].index(st.session_state.pagina_atual))

        if op != st.session_state.pagina_atual:
            st.session_state.pagina_atual = op
            st.rerun()

        df = cls.carregar_dados()

        if op == "Dados":
            Dados.main(df)
        elif op == "Médias":
            Médias.main(df)
        elif op == "Operações":
            Operações.main(df)

IndexUI.main()
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
        while True:
            df = cls.carregar_dados()
            op = st.sidebar.selectbox("MENU:", ["Dados", "Médias", "Operações"])
            
            if op == "Dados":
                Dados.main(df)
            elif op == "Médias":
                Médias.main(df)
            elif op == "Operações":
                Operações.main(df)
            else:
                Dados.main(df[df["Cliente"] == op])
            
            time.sleep(5)
            st.rerun()  

IndexUI.main()
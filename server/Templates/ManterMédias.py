import streamlit as st
#import pandas as pd


class Médias:
    @staticmethod
    def main(df):
        st.header("Selecione alguma das operações:")
        st.subheader("Médias")

        t1, t2, t3, t4 = st.tabs([
            "Processadores", "Memória RAM Livre", "Espaço em Disco Livre", "Temperatura CPU"
        ])

        with t1:
            Médias.processadores(df)
        with t2: 
            Médias.memoria_ram(df)
        with t3: 
            Médias.espaco_disco(df)
        with t4:
            Médias.temperatura(df)

    @staticmethod
    def temperatura(df):        
        st.subheader("Temperatura CPU")
        if "Temperatura CPU" not in df.columns:
            st.info("'Temperatura CPU' não encontrada no DataFrame.")
        elif df["Temperatura CPU"].isnull().all():
            st.write("Nenhum dado disponível para temperatura.")
        else:
            media = df["Temperatura CPU"].mean()
            st.write(f'Média de Temperatura CPU: {media:.2f}°C')
            st.bar_chart(df.set_index("Cliente")["Temperatura CPU"])

    @staticmethod
    def processadores(df):        
        st.subheader("Processadores")
        if "Processadores" not in df.columns:
            st.info("'Processadores' não encontrada no DataFrame.")
        else:
            media = df["Processadores"].mean()
            st.write(f'Média da quantidade de processadores: {media:.2f}')
            st.bar_chart(df.set_index("Cliente")["Processadores"])

    @staticmethod
    def memoria_ram(df):        
        st.subheader("Memória RAM Livre")
        if "Memória RAM Livre (GB)" not in df.columns:
            st.info("'Memória RAM Livre (GB)' não encontrada no DataFrame.")
        else:
            media = df["Memória RAM Livre (GB)"].mean()
            st.write(f'Média de Memória RAM Livre: {media:.2f} GB')
            st.bar_chart(df.set_index("Cliente")["Memória RAM Livre (GB)"])

    @staticmethod
    def espaco_disco(df):        
        st.subheader("Espaço Livre em Disco")
        if "Espaço em Disco Livre (GB)" not in df.columns:
            st.info("'Espaço em Disco Livre (GB)' não encontrada no DataFrame.")
        else:
            media = df["Espaço em Disco Livre (GB)"].mean()
            st.write(f'Média de Espaço em Disco Livre: {media:.2f} GB')
            st.bar_chart(df.set_index("Cliente")["Espaço em Disco Livre (GB)"])

import streamlit as st
#import pandas as pd
import json
class Operações:
    def main(df):
        st.header("Selecione alguma das operações:")
        st.subheader("Operações")

        # Abas para as operações
        t1, t2 = st.tabs(["doomsday RAM", "Desligar maquina"])

        with t1:

            Operações.doomsdayRAM(df)

        with t2:

            Operações.desligarmaquina(df)

    def desligarmaquina(df):
        op = None
        if 'Cliente' in df.columns and not df['Cliente'].empty:
            op = st.selectbox(
                "Escolha um cliente", 
                df['Cliente'].tolist(),
                key="desligar"
            )
        else:
            st.info('Nenhum cliente disponivel')
            
        if st.button("desligar",key="des") and op:
            acao = {
                "cliente": op,
                "comando": "shutdown"
            }

            try:
                with open("comandos.json", "r") as file:
                    comandos = json.load(file)
            except FileNotFoundError:
                comandos = []

            comandos.append(acao)

            with open("comandos.json", "w") as file:
                json.dump(comandos, file, indent=4)
            st.write("Comando enviado!")

    def doomsdayRAM(df):
        op = None
        if 'Cliente' in df.columns and not df['Cliente'].empty:
            op = st.selectbox(
                "Escolha um cliente", 
                df['Cliente'].tolist(),
                key="doomsday_ram"
            )
        else:
            st.info('Nenhum cliente disponivel')

        if st.button("consumir memoria ram",key="doomsday_ramb" and op):
            acao = {
                "cliente": op,
                "comando": "deathram"
            }

            try:
                with open("comandos.json", "r") as file:
                    comandos = json.load(file)
            except FileNotFoundError:
                comandos = []

            comandos.append(acao)

            with open("comandos.json", "w") as file:
                json.dump(comandos, file, indent=4)
            st.write("Comando enviado!")
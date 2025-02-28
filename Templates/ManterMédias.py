import streamlit as st
#import pandas as pd

class Médias:
    def main(self, df):

        st.header("Selecione alguma das operações:")
        st.subheader(f"{self}")

        t1, t2, t3, t4 = st.tabs(["Quantidade de processadores", "Memória Ram Livre", "Espaço em disco livre", "Temperatura"])

        with t1 : Médias.processadores(df)
        with t2 : Médias.memóriaRAM(df)
        with t3 : Médias.espaçoDisco(df)
        with t4 : Médias.temperatura(df)

    def apagarNada(df):
        st.dataframe(df)
    
    def temperatura(df):        
        st.subheader("Temperatura")
        soma = sum(df['temperatura'])
        media = soma/(len(df['temperatura']))
        st.write(f'Média de temperatura: {media}')
        st.bar_chart(df.set_index("clientes")["temperatura"])

    def processadores(df):        
        st.subheader("Processadores")
        soma = sum(df['Quantidade de processadores'])
        media = soma/(len(df['Quantidade de processadores']))
        st.write(f'Média da quantidade de processadores {media}')
        st.bar_chart(df.set_index("clientes")["Quantidade de processadores"])

    def memóriaRAM(df):        
        st.subheader("Memória RAM Livre")
        soma = sum(df['Memória Ram Livre (GB)'])
        media = soma/(len(df['Memória Ram Livre (GB)']))
        st.write(f'Média da Memória Ram Livre (GB) {media}')
        st.bar_chart(df.set_index("clientes")["Memória Ram Livre (GB)"])

    def espaçoDisco(df):        
        st.subheader("Espaço livre no disco")
        soma = sum(df['Espaço em disco livre (GB)'])
        media = soma/(len(df['Espaço em disco livre (GB)']))
        st.write(f'Média da Espaço em disco livre (GB) {media}')
        st.bar_chart(df.set_index("clientes")["Espaço em disco livre (GB)"])
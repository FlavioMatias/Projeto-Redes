import streamlit as st
#import pandas as pd

class Operações:
    def main(df):

        st.header("Selecione alguma das operações:")
        st.subheader("Operações")

        t1, t2, t3 = st.tabs(["Apagar dados", "Desligar o pc", "Abrir Janelas"])

        with t1 : Operações.apagarDados(df)
        with t2 : Operações.apagarNada(df)
        with t3 : Operações.apagarNada(df)



    def apagarNada(df):
        st.dataframe(df)

    def apagarDados(df):
        st.selectbox(
            "Escolha um cliente", 
            df['Cliente'].tolist()  # Convertendo a coluna 'clientes' para uma lista
        )

        if st.button("Apagar"):
            st.write("Você apagou com sucesso!")
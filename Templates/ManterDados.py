import streamlit as st

class Dados:
    def main(self, df):
        st.header("Dados dos clientes:")
        for _, linha in df.iterrows():
            with st.container(border=True):
                st.write(f"Cliente: {linha['clientes']}")
                st.write(f"Temperatura: {linha['temperatura']}")
                st.write(f"Quantidade de processadores: {linha['Quantidade de processadores']}")
                st.write(f"Memória RAM livre: {linha['Memória Ram Livre (GB)']} GB")
                st.write(f"Espaço livre em disco: {linha['Espaço em disco livre (GB)']} GB")
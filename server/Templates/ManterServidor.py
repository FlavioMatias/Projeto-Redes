import streamlit as st

class Servidor:
    def main(df):
        st.header("Dados do servidor:")
        for _, linha in df.iterrows():
            with st.container(border=True):
                with st.expander("TCP"):
                    TCP = "192.168.1.100:5050"
                    st.write(f"Ativo: {True}")
                    st.write(f"TCP: {TCP}")
                    
                with st.expander("Broadcast"):
                    broadcast = "255.255.255.255:5000"
                    st.write(f"Ativo: {True}")
                    st.write(f"Broadcast: {broadcast}")
            

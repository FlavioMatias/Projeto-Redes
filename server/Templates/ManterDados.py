import streamlit as st

class Dados:
    def main(df):
        st.header("Dados dos clientes:")
        for _, linha in df.iterrows():
            with st.container(border=True):
                st.subheader(f"Cliente: {linha['Cliente']}")
                with st.expander("Informações do Sistema"):
                    st.write(f"Hostname: {linha['Hostname']}")
                    st.write(f"Sistema Operacional: {linha['Sistema Operacional']}")
                    st.write(f"Arquitetura: {linha['Arquitetura']}")
                with st.expander("Hardware"):
                    st.write(f"Quantidade de Processadores: {linha['Processadores']}")
                    st.write(f"Frequência da CPU: {linha['Frequência CPU (MHz)']} MHz")
                    st.write(f"Temperatura da CPU: {linha['Temperatura CPU']}°C")
                    st.write(f"Memória RAM Total: {linha['Memória RAM Total (GB)']} GB")
                    st.write(f"Memória RAM Livre: {linha['Memória RAM Livre (GB)']} GB")
                with st.expander("Disco"):
                    st.write(f"Espaço Total em Disco: {linha['Espaço em Disco Total (GB)']} GB")
                    st.write(f"Espaço Livre em Disco: {linha['Espaço em Disco Livre (GB)']} GB")
                with st.expander("Uso do Sistema"):
                    st.write(f"Uso de CPU: {linha['Uso CPU (%)']}%")
                    st.write(f"Uso de RAM: {linha['Uso RAM (%)']}%")
                    st.write(f"Uso de Disco: {linha['Uso Disco (%)']}%")
                with st.expander("Rede e Conectividade"):
                    st.write(f"IP Local: {linha['IP Local']}")
                    st.write(f"IP Público: {linha['IP Público']}")
                    st.write(f"MAC Address: {linha['MAC Address']}")
                    st.write(f"Latência para o Google: {linha['Latência Google (ms)']} ms")
                with st.expander("Bateria"):
                    st.write(f"Nível da Bateria: {linha['Nível Bateria (%)']}%")
                    st.write(f"Carregando: {'Sim' if linha['Carregando'] else 'Não'}")

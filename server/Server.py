import socket
import json
import threading
import time
import os
import platform
import subprocess
from cryptography.fernet import Fernet  # Importando a biblioteca de criptografia

CryptKey = 'XXHQzo1N9eKRkpw3dhLurZ6c2qK9w5W7smB2UmFXTl0='
BROADCAST_PORT = 50000
TCP_PORT = 50001
BROADCAST_MESSAGE = "FGG".encode()
DATA_FILE = "data.json"

class Server:
    @staticmethod
    def liberar_portas():
        """Libera as portas fechando processos que estejam utilizando-as."""
        sistema = platform.system()
        
        if sistema == "Windows":
            for port in [BROADCAST_PORT, TCP_PORT]:
                comando = f"netstat -ano | findstr :{port}"
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                linhas = resultado.stdout.strip().split("\n")
                
                for linha in linhas:
                    partes = linha.split()
                    if len(partes) >= 5:
                        pid = partes[-1]
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True)

        elif sistema in ["Linux", "Darwin"]:
            for port in [BROADCAST_PORT, TCP_PORT]:
                comando = f"lsof -ti :{port}"
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                pids = resultado.stdout.strip().split("\n")
                
                for pid in pids:
                    if pid.isdigit():
                        subprocess.run(f"kill -9 {pid}", shell=True)

    @staticmethod
    def broadcast_pings():
        """Envia pings em broadcast periodicamente."""
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            udp_sock.sendto(BROADCAST_MESSAGE, ('<broadcast>', BROADCAST_PORT))
            print('ping...')
            time.sleep(5)

    @staticmethod
    def data_receive():
        """Abre um servidor TCP que recebe dados e salva em um arquivo JSON."""

        cipher_suite = Fernet(CryptKey)

        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        tcp_sock.bind(('0.0.0.0', TCP_PORT))
        tcp_sock.listen(5)
        print("TCP server iniciado, aguardando conexões...")

        while True:
            conn, addr = tcp_sock.accept()
            data = conn.recv(4096)
            if data:
                try:
                    # Descriptografa os dados recebidos
                    dados_descriptografados = cipher_suite.decrypt(data)
                    json_data = json.loads(dados_descriptografados.decode())
                    Server.save_data(addr[0], json_data)
                except Exception as e:
                    print("Servidor: Erro ao decodificar ou descriptografar dados:", e)
            conn.close()

    @staticmethod
    def save_data(client_ip, data):
        """Salva os dados no arquivo JSON, sobrescrevendo os dados do mesmo cliente."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    all_data = json.load(file)
                except json.JSONDecodeError:
                    all_data = {}
        else:
            all_data = {}

        all_data[client_ip] = data
        with open(DATA_FILE, "w") as file:
            json.dump(all_data, file, indent=4)

        print(f"Servidor: Dados do cliente {client_ip} armazenados em {DATA_FILE}")

    @staticmethod
    def start():
        """Inicia o servidor com todas as funcionalidades em threads separadas."""
        Server.liberar_portas()
        threading.Thread(target=Server.broadcast_pings, daemon=True).start()
        threading.Thread(target=Server.data_receive, daemon=True).start()
        
        while True:
            time.sleep(1)

Server.start()
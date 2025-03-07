import socket
import json
import threading
import time
import os
import platform
import subprocess
from cryptography.fernet import Fernet

# Configurações
CryptKey = 'XXHQzo1N9eKRkpw3dhLurZ6c2qK9w5W7smB2UmFXTl0=' 
BROADCAST_PORT = 50000  
TCP_PORT = 50001 
BROADCAST_MESSAGE = "FGG".encode()  
DATA_FILE = "data.json"  
COMANDOS_FILE = "comandos.json"  

class Server:
    clientes_conectados = {}  

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
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET) 
        allips = [ip[-1][0] for ip in interfaces] 
        while True:
            for ip in allips:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
                sock.bind((ip,0))
                sock.sendto(BROADCAST_MESSAGE, ("255.255.255.255", BROADCAST_PORT))
                sock.close()
            time.sleep(5)

    @staticmethod
    def handle_client(conn, addr):
        """Lida com a conexão de um cliente específico."""
        cipher_suite = Fernet(CryptKey)
        print(f"Conexão estabelecida com {addr}")
        Server.clientes_conectados[addr[0]] = conn

        while True:
            try:
                data = conn.recv(4096)  
                if not data:
                    break  
                dados_descriptografados = cipher_suite.decrypt(data)
                json_data = json.loads(dados_descriptografados.decode())

                Server.save_data(addr[0], json_data)

            except Exception as e:
                print(f"Erro ao lidar com o cliente {addr}: {e}")
                break

        if addr[0] in Server.clientes_conectados:
            del Server.clientes_conectados[addr[0]]
        Server.remove_data(addr[0])
        conn.close()
        print(f"Conexão com {addr} encerrada")

    @staticmethod
    def data_receive():
        """Abre um servidor TCP que recebe dados e lida com múltiplos clientes."""
        cipher_suite = Fernet(CryptKey)

        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind(('0.0.0.0', TCP_PORT))
        tcp_sock.listen(5)
        print("TCP server iniciado, aguardando conexões...")

        while True:
            conn, addr = tcp_sock.accept()
            threading.Thread(target=Server.handle_client, args=(conn, addr), daemon=True).start()

    @staticmethod
    def processar_comandos():
        """Lê o arquivo JSON de comandos e envia os comandos aos clientes."""
        while True:
            try:
                with open(COMANDOS_FILE, "r") as file:
                    comandos = json.load(file)

                for comando in comandos:
                    cliente = comando["cliente"]
                    cmd = comando["comando"]

                    if cliente in Server.clientes_conectados:
                        conn = Server.clientes_conectados[cliente]
                        Server.enviar_comando(conn, cliente, cmd)
                        print(f"Comando '{cmd}' enviado para o cliente {cliente}.")

                with open(COMANDOS_FILE, "w") as file:
                    json.dump([], file)

            except FileNotFoundError:
                print("Arquivo de comandos não encontrado. Criando um novo...")
                with open(COMANDOS_FILE, "w") as file:
                    json.dump([], file)
            except Exception as e:
                print(f"Erro ao processar comandos: {e}")

            time.sleep(5)

    @staticmethod
    def enviar_comando(conn, ip, comando):
        """Envia o comando criptografado para o IP via o socket já conectado."""
        try:
            cipher_suite = Fernet(CryptKey)
            encrypted_command = cipher_suite.encrypt(comando.encode())
            conn.sendall(encrypted_command)
            print(f"Comando '{comando}' enviado para {ip}")
        except Exception as e:
            print(f"Erro ao enviar comando para {ip}: {e}")

    @staticmethod
    def save_data(client_ip, data):
        """Salva os dados no arquivo JSON, mantendo apenas clientes conectados."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    all_data = json.load(file)
                except json.JSONDecodeError:
                    all_data = {}
        else:
            all_data = {}

        all_data[client_ip] = data

        connected_ips = Server.clientes_conectados.keys()
        all_data = {ip: all_data[ip] for ip in all_data if ip in connected_ips}

        with open(DATA_FILE, "w") as file:
            json.dump(all_data, file, indent=4)

        print(f"Dados do cliente {client_ip} armazenados")

    @staticmethod
    def remove_data(client_ip):
        """Remove os dados de um cliente desconectado do arquivo JSON."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    all_data = json.load(file)
                except json.JSONDecodeError:
                    all_data = {}
        else:
            all_data = {}

        # Remove o cliente do JSON
        if client_ip in all_data:
            del all_data[client_ip]

        # Salva os dados atualizados no arquivo JSON
        with open(DATA_FILE, "w") as file:
            json.dump(all_data, file, indent=4)

        print(f"Dados do cliente {client_ip} removidos")

    @staticmethod
    def start():
        """Inicia o servidor com todas as funcionalidades em threads separadas."""
        Server.liberar_portas()
        threading.Thread(target=Server.broadcast_pings, daemon=True).start()
        threading.Thread(target=Server.data_receive, daemon=True).start()
        threading.Thread(target=Server.processar_comandos, daemon=True).start()
        
        while True:
            time.sleep(1)

if __name__ == "__main__":
    Server.start()
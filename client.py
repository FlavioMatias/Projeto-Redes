import socket
import json
import time
import psutil
import platform
import uuid
import requests
from cryptography.fernet import Fernet

BROADCAST_PORT = 50000
TCP_PORT = 50001

class Client:
    @staticmethod
    def load_key():
        """Carrega a chave de criptografia do arquivo."""
        with open("chave.key", "rb") as filekey:
            return filekey.read()

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
            return addr[0]
        return None

    @staticmethod
    def get_public_ip():
        """Obtém o endereço IP público do cliente."""
        try:
            return requests.get("https://api64.ipify.org").text
        except:
            return "Desconhecido"

    @staticmethod
    def get_system_info():
        """Coleta informações detalhadas do sistema."""
        num_processadores = psutil.cpu_count()
        ram_total = round(psutil.virtual_memory().total / (1024**3), 2)
        ram_livre = round(psutil.virtual_memory().available / (1024**3), 2)
        disco_total = round(psutil.disk_usage('/').total / (1024**3), 2)
        disco_livre = round(psutil.disk_usage('/').free / (1024**3), 2)
        uso_cpu = psutil.cpu_percent(interval=1)
        uso_ram = psutil.virtual_memory().percent
        uso_disco = psutil.disk_usage('/').percent

        # Verifica se a função sensors_temperatures() está disponível (exclusivo do Linux)
        temp_processador = None
        if hasattr(psutil, 'sensors_temperatures'):
            temperaturas = psutil.sensors_temperatures()
            if 'coretemp' in temperaturas:
                temp_processador = round(sum(temp.current for temp in temperaturas['coretemp']) / len(temperaturas['coretemp']), 1)
        else:
            temp_processador = "Indisponível (não suportado no Windows)"

        ip_local = socket.gethostbyname(socket.gethostname())
        ip_publico = Client.get_public_ip()
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])

        # Verifica se a interface de rede 'Wi-Fi' está disponível (pode variar no Windows)
        velocidade_rede = "Desconhecida"
        if 'Wi-Fi' in psutil.net_if_stats():
            velocidade_rede = psutil.net_if_stats()['Wi-Fi'].speed
        else:
            # Tenta obter a velocidade da primeira interface de rede disponível
            interfaces = psutil.net_if_stats()
            for interface in interfaces:
                if interfaces[interface].isup:
                    velocidade_rede = interfaces[interface].speed
                    break

        # Tenta obter a latência do ping (pode não funcionar no Windows sem permissões)
        latencia = "Indisponível"
        try:
            ping_google = psutil.subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True)
            latencia = float([x for x in ping_google.stdout.split("\n") if "time=" in x][0].split("time=")[1].split(" ")[0])
        except:
            latencia = "Indisponível"

        # Informações sobre bateria (pode não estar disponível em desktops)
        nivel_bateria = "Sem bateria"
        carregando = False
        if hasattr(psutil, 'sensors_battery'):
            bateria = psutil.sensors_battery()
            if bateria:
                nivel_bateria = round(bateria.percent, 1)
                carregando = bateria.power_plugged

        return {
            "hostname": platform.node(),
            "sistema_operacional": platform.system(),
            "arquitetura": platform.architecture()[0],
            "usuario": platform.uname().node,

            # Hardware
            "processadores": num_processadores,
            "frequencia_cpu_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else "Desconhecido",
            "ram_total_gb": ram_total,
            "ram_livre_gb": ram_livre,
            "disco_total_gb": disco_total,
            "disco_livre_gb": disco_livre,
            "uso_cpu_percent": uso_cpu,
            "uso_ram_percent": uso_ram,
            "uso_disco_percent": uso_disco,
            "temperatura_cpu": temp_processador,

            # Rede
            "ip_local": ip_local,
            "ip_publico": ip_publico,
            "mac_address": mac_address,
            "velocidade_rede_mbps": velocidade_rede,
            "latencia_google_ms": latencia,

            # Bateria
            "nivel_bateria": nivel_bateria,
            "carregando": carregando,
        }

    @staticmethod
    def send_data(server_ip):
        """Envia um JSON com dados do sistema para o servidor a cada 5 segundos."""
        # Carrega a chave de criptografia
        chave = Client.load_key()
        cipher_suite = Fernet(chave)

        while True:
            try:
                tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_sock.connect((server_ip, TCP_PORT))

                # Coleta os dados do sistema
                dados_sistema = Client.get_system_info()
                json_message = json.dumps(dados_sistema)

                # Criptografa os dados
                dados_criptografados = cipher_suite.encrypt(json_message.encode())

                # Envia os dados criptografados
                tcp_sock.send(dados_criptografados)
                print(f"Cliente: Dados enviados para o servidor {server_ip}")
                tcp_sock.close()
            except Exception as e:
                print(e)

            time.sleep(5)  

if __name__ == "__main__":
    server_ip = Client.get_server_ip()
    if server_ip:
        Client.send_data(server_ip)
    else:
        print("Cliente: Nenhum servidor encontrado. Encerrando.")
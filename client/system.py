import psutil
import platform
import uuid
import requests
import socket
import subprocess
import threading
import time

class System:
    @staticmethod
    def get_public_ip():
        """Obtém o endereço IP público do cliente."""
        try:
            return requests.get("https://api64.ipify.org").text
        except:
            return "Desconhecido"

    @staticmethod
    def get_cpu_info():
        temp_processador = "Indisponível"
        if hasattr(psutil, 'sensors_temperatures'):
            temperaturas = psutil.sensors_temperatures()
            if 'coretemp' in temperaturas:
                temp_processador = round(sum(temp.current for temp in temperaturas['coretemp']) / len(temperaturas['coretemp']), 1)
        
        return {
            "processadores": psutil.cpu_count(),
            "frequencia_cpu_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else "Desconhecido",
            "uso_cpu_percent": psutil.cpu_percent(interval=1),
            "temperatura_cpu": temp_processador
        }

    @staticmethod
    def get_memory_info():
        ram = psutil.virtual_memory()
        return {
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "ram_livre_gb": round(ram.available / (1024**3), 2),
            "uso_ram_percent": ram.percent
        }
    
    @staticmethod
    def get_disk_info():
        disco = psutil.disk_usage('/')
        return {
            "disco_total_gb": round(disco.total / (1024**3), 2),
            "disco_livre_gb": round(disco.free / (1024**3), 2),
            "uso_disco_percent": disco.percent
        }

    @staticmethod
    def get_network_info():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
        latencia = "Indisponível"
        try:
            ping_google = psutil.subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True)
            latencia = float([x for x in ping_google.stdout.split("\n") if "time=" in x][0].split("time=")[1].split(" ")[0])
        except:
            latencia = "Indisponível"
        
        return {
            "ip_local": socket.gethostbyname(socket.gethostname()),
            "ip_publico": System.get_public_ip(),
            "mac_address": mac_address,
            "latencia_google_ms": latencia
        }
    
    @staticmethod
    def get_battery_info():
        nivel_bateria = "Sem bateria"
        carregando = False
        if hasattr(psutil, 'sensors_battery'):
            bateria = psutil.sensors_battery()
            if bateria:
                nivel_bateria = round(bateria.percent, 1)
                carregando = bateria.power_plugged
        return {"nivel_bateria": nivel_bateria, "carregando": carregando}

    @staticmethod
    def get_system_info():
        """Coleta todas as informações do sistema."""
        return {
            "hostname": platform.node(),
            "sistema_operacional": platform.system(),
            "arquitetura": platform.architecture()[0],
            "usuario": platform.uname().node,
            **System.get_cpu_info(),
            **System.get_memory_info(),
            **System.get_disk_info(),
            **System.get_network_info(),
            **System.get_battery_info()
        }
    @staticmethod
    def process_cmd(cmd):
        """Processa os comandos recebidos, como 'shutdown' para desligar a máquina."""
        print(f'Comando requisitado: {cmd}')
        match cmd:
            case "shutdown":
                sistema = platform.system()
                if sistema == "Windows":
                    print("Cliente: Desligando a máquina... (Windows)")
                    subprocess.run("shutdown /s /f /t 0", shell=True)
                elif sistema == "Linux" or sistema == "Darwin":  # Inclui macOS
                    print("Cliente: Desligando a máquina... (Linux/macOS)")
                    subprocess.run("shutdown -h now", shell=True)
                else:
                    print(f"Cliente: Sistema {sistema} não suportado para o comando shutdown.")

            case "logout":
                sistema = platform.system()
                if sistema == "Windows":
                    print("Cliente: Encerrando sessão... (Windows)")
                    subprocess.run("shutdown /l", shell=True)
                elif sistema == "Linux" or sistema == "Darwin":
                    print("Cliente: Encerrando sessão... (Linux/macOS)")
                    subprocess.run("logout", shell=True)
                else:
                    print(f"Cliente: Sistema {sistema} não suportado para o comando logout.")
            case 'deathram':
                def consume():
                    size = 10**7  # 10 MB (tamanho inicial do bloco)
                    min_memory = 10 * 1024 * 1024  # 10 MB (limite de memória livre)
                    data = []

                    while True:
                        try:
                            # Verifica a memória disponível
                            mem = psutil.virtual_memory()
                            if mem.available <= min_memory:
                                print(f"Memória livre atingiu o limite de {min_memory / (1024 ** 2):.2f} MB. Parando thread.")
                                break

                            # Aloca memória
                            data.append(bytearray(size))
                            print(f"Alocados {size} bytes. Memória usada: {mem.used / (1024 ** 2):.2f} MB")

                            # Pausa para evitar consumo excessivo
                            time.sleep(0.05)  # Pausa de 0.5 segundos

                        except MemoryError:
                            print("Memória esgotada. Parando thread.")
                            break
                threads = []
                for _ in range(2):  
                    t = threading.Thread(target=consume)
                    t.start()
                    threads.append(t)

                for t in threads:
                    t.join()
            case _:
                print(f"Cliente: Comando '{cmd}' não reconhecido.")
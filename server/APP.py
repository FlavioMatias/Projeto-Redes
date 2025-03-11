import subprocess
import os
import sys
import platform
import signal
import time

class APP:
    @staticmethod
    def update_pip():
        """Atualiza o pip para a versão mais recente."""
        print("Atualizando pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    @staticmethod
    def install_pipreqs():
        """Instala o pipreqs se não estiver instalado."""
        try:
            import pipreqs
        except ImportError:
            print("pipreqs não encontrado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pipreqs"])

    @staticmethod
    def generate_requirements():
        """Gera o arquivo requirements.txt usando pipreqs."""
        print("Gerando requirements.txt com pipreqs...")
        subprocess.run([sys.executable, "-m", "pipreqs.pipreqs", ".", "--encoding=utf8", "--force"], check=True)

    @staticmethod
    def install_requirements():
        """Instala as dependências listadas no requirements.txt."""
        print("Instalando dependências...")
        subprocess.run(["pip", "install", "-r", "requirements.txt"])

    @staticmethod
    def Run():
        """Configura o ambiente e executa o aplicativo."""
        # Atualiza o pip antes de qualquer coisa
        APP.update_pip()

        APP.install_pipreqs()

        APP.generate_requirements()

        APP.install_requirements()

        # Inicia o Streamlit
        print("Iniciando Streamlit...")
        streamlit_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "server/IndexUI.py"])

        # Inicia o servidor
        print("Iniciando servidor...")
        server_process = subprocess.Popen([sys.executable, "server/Server.py"])

        # Função para lidar com o sinal de interrupção (Ctrl+C)
        def signal_handler(sig, frame):
            print("\nInterrompendo subprocessos...")
            streamlit_process.terminate()  # Envia SIGTERM para o processo do Streamlit
            server_process.terminate()     # Envia SIGTERM para o processo do servidor
            streamlit_process.wait()       # Espera o processo do Streamlit terminar
            server_process.wait()          # Espera o processo do servidor terminar
            print("Subprocessos interrompidos. Saindo...")
            sys.exit(0)

        # Configura o handler para o sinal SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, signal_handler)

        # Mantém o script principal em execução enquanto os subprocessos estiverem ativos
        try:
            while streamlit_process.poll() is None or server_process.poll() is None:
                time.sleep(0.5)  # Espera para evitar uso excessivo da CPU
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    APP.Run()
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
    def setup_environment():
        """Configura o ambiente virtual e instala as dependências."""
        print("Instalando dependências...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    @staticmethod
    def Run():
        """Configura o ambiente e executa o aplicativo."""
        # Atualiza o pip antes de qualquer coisa
        APP.update_pip()

        APP.install_pipreqs()

        APP.generate_requirements()

        APP.setup_environment()

        # Inicia o subprocesso
        process = subprocess.Popen([sys.executable, "client/client.py"])

        # Função para lidar com o sinal de interrupção (Ctrl+C)
        def signal_handler(sig, frame):
            print("\nInterrompendo o subprocesso...")
            process.terminate()  # Envia SIGTERM para o subprocesso
            process.wait()       # Espera o subprocesso terminar
            print("Subprocesso interrompido. Saindo...")
            sys.exit(0)

        # Configura o handler para o sinal SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, signal_handler)

        # Mantém o script principal em execução enquanto o subprocesso estiver ativo
        try:
            while process.poll() is None:
                time.sleep(0.5)  # Espera para evitar uso excessivo da CPU
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    APP.Run()
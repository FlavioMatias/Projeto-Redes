import subprocess
import os
import sys
import platform


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
        subprocess.run(["pip", "install", "-r", "requirements.txt"])

    @staticmethod
    def Run():
        """Configura o ambiente e executa o aplicativo."""
        # Atualiza o pip antes de qualquer coisa
        APP.update_pip()

        APP.install_pipreqs()

        APP.generate_requirements()

        APP.install_requirements()

        print("Iniciando Streamlit...")
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "server/IndexUI.py"])

        print("Iniciando servidor...")
        subprocess.Popen([sys.executable, "server/Server.py"])

if __name__ == '__main__':
    APP.Run()
import subprocess
import os
import sys
import platform
from Server import Server

class APP:
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
        subprocess.run([sys.executable, "-m", "pipreqs", ".", "--encoding=utf8", "--force"])

    @staticmethod
    def setup_environment():
        """Configura o ambiente virtual e instala as dependências."""
        venv_name = "venv"

        if not os.path.exists(venv_name):
            print("Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", venv_name])

        if platform.system() == "Windows":
            activate_script = os.path.join(venv_name, "Scripts", "activate")
            python_exec = os.path.join(venv_name, "Scripts", "python.exe")
        else:  # Linux ou MacOS
            activate_script = os.path.join(venv_name, "bin", "activate")
            python_exec = os.path.join(venv_name, "bin", "python3")

        print("Instalando dependências...")
        subprocess.run([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])

        return python_exec

    @staticmethod
    def Run():
        """Configura o ambiente e executa o aplicativo."""
        APP.install_pipreqs()

        APP.generate_requirements()

        python_exec = APP.setup_environment()

        print("Iniciando Streamlit...")
        subprocess.Popen([python_exec, "-m", "streamlit", "run", "server/IndexUI.py"])

        print("Iniciando servidor...")
        Server.start()

if __name__ == '__main__':
    APP.Run()
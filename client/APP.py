import subprocess
import os
import sys
import platform
from client import Client

class APP:
    @staticmethod
    def install_pipreqs():
        """Instala o pipreqs se não estiver instalado."""
        try:
            import pipreqs
        except ImportError:
            print("pipreqs não encontrado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pipreqs"], check=True)

    @staticmethod
    def generate_requirements():
        """Gera o arquivo requirements.txt usando pipreqs."""
        print("Gerando requirements.txt com pipreqs...")
        try:
            subprocess.run([sys.executable, "-m", "pipreqs.pipreqs", ".", "--encoding=utf8", "--force"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao gerar requirements.txt: {e}")
            sys.exit(1)

    @staticmethod
    def setup_environment():
        """Configura o ambiente virtual e instala as dependências."""
        venv_name = "venv"

        if not os.path.exists(venv_name):
            print("Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)

        if platform.system() == "Windows":
            activate_script = os.path.join(venv_name, "Scripts", "activate")
            python_exec = os.path.join(venv_name, "Scripts", "python.exe")
        else:  # Linux ou MacOS
            activate_script = os.path.join(venv_name, "bin", "activate")
            python_exec = os.path.join(venv_name, "bin", "python3")

        print("Instalando dependências...")
        subprocess.run([python_exec, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

        return python_exec

    @staticmethod
    def Run():
        """Configura o ambiente e executa o aplicativo."""
        try:
            APP.install_pipreqs()
            APP.generate_requirements()
            python_exec = APP.setup_environment()

            # Executa o cliente
            print("Iniciando cliente...")
            Client.run()
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            sys.exit(1)

if __name__ == '__main__':
    APP.Run()
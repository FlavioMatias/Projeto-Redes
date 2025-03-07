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
        # Atualiza o pip antes de qualquer coisa
        APP.update_pip()

        APP.install_pipreqs()

        APP.generate_requirements()

        python_exec = APP.setup_environment()

        subprocess.Popen([python_exec, "client/client.py"])

if __name__ == '__main__':
    APP.Run()
import subprocess

class APP:
    @staticmethod
    def Run():
        # Rodar o servidor como subprocesso
        subprocess.Popen(['python3', 'server/Server.py'])
        
        # Rodar o Streamlit com o comando correto
        subprocess.Popen(['python3', '-m', 'streamlit', 'run', 'server/IndexUI.py'])

if __name__ == '__main__':
    APP.Run()

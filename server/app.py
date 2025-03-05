import subprocess
from Server import Server
class APP:
    @staticmethod
    def Run():
        subprocess.Popen(['python3', '-m', 'streamlit', 'run', 'server/IndexUI.py'])
        Server.start()

if __name__ == '__main__':
    APP.Run()

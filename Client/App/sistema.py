from psutil import *
import os
import platform

class System:
    
    @staticmethod
    def request(cmd : str):
        
        match cmd:
            case  '/kill':
                
                sistema = platform.system()
    
                if sistema == "Windows":
                    os.system("shutdown /s /t 0")
                elif sistema == "Linux" or sistema == "Darwin":  # Darwin = macOS
                    os.system("sudo shutdown -h now")

            
            
    @staticmethod
    def memoryFree():
        mem = virtual_memory()
        return float(f'{mem.available / (1024**3):.2f}')
    
System.request('/kill')

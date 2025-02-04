import socket
import psutil
import time
import json

while True:
  data = {
    "cpu_qtd": psutil.cpu_count(),
    "memory": psutil.virtual_memory()._asdict(),
    "disk": psutil.disk_usage("/")._asdict(),
  }

  print(json.dumps(data, indent=4))

  time.sleep(10)
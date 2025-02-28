from cryptography.fernet import Fernet

chave = Fernet.generate_key()

with open("chave.key", "wb") as filekey:
    filekey.write(chave)
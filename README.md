<div style="text-align: center;">
    # **Projeto Redes - Monitoramento de Hardware**
</div>

## Descrição  

Este repositório contém os códigos e arquivos utilizados no desenvolvimento do projeto proposto pelo professor **Ivanilson** na disciplina de **Redes de Computadores**.  

O objetivo do projeto é implementar um **sistema cliente-servidor** que permite a **coleta e monitoramento remoto de informações de hardware** de máquinas clientes. O servidor recebe dados como:  

- 🖥 **Quantidade de processadores**  
- 💾 **Memória RAM livre e total**  
- 📂 **Espaço em disco livre e total**  
- 🌡 **Temperatura do processador**  

Além disso, o sistema calcula a **média dos dados coletados** e permite que o administrador visualize informações de clientes específicos.  

---

## ⚙️ **Tecnologias Utilizadas**  
- **Python** 🐍 – Linguagem principal do projeto  
- **Socket** 🔌 – Comunicação cliente-servidor  
- **Streamlit** 🎨 – Interface gráfica para visualização de dados
  
---

## **Funcionalidades Principais**  
✅ Comunicação Cliente-Servidor via **sockets puros**  
✅ Monitoramento **em tempo real** dos clientes  
✅ Interface web intuitiva para análise de dados  
✅ Suporte a **criptografia** para garantir a segurança da comunicação  
✅ Armazenamento em **JSON**, eliminando necessidade de banco de dados tradicional  

---

## 📂 **Estrutura do Repositório**  

***EM BREVE***

## **Como Executar o Projeto**  

### **Pré-requisitos**  
Antes de iniciar, certifique-se de ter o **Python 3.8+** instalado.  

### **Instalação e Execução**  

1️⃣ Clone o repositório:  
```bash
git clone https://github.com/FlavioMatias/Projeto-Redes.git
cd Projeto-Redes
```

2️⃣ Instale as dependências:  
```bash
pip install -r requisitos.txt
```

3️⃣ Inicie o sistema do servidor:  
```bash
python main.py
```

4️⃣ Inicie o cliente (em outra máquina ou terminal):  
```bash
python client.py
```

---

## 👨‍💻 **Contribuidores**  
**Desenvolvido por:**
    [Flavio Matias]()
    [Gustavo Tavares]()
    [Gustavo Maia]()
    
**Orientação:** Professor **Ivanilson**  

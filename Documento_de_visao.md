## Sistema de Coleta de Dados via Servidor na Camada de Enlace

### Histórico da Revisão

| Data       | Versão | Descrição         |
|------------|--------|------------------|
| 30/06/2025 | **1.00** | Versão Inicial |

---

### 1. Objetivo do Projeto

O projeto tem como objetivo coletar e monitorar dados do hardware de clientes conectados a um servidor, incluindo:
- Quantidade de processadores;
- Memória RAM livre e total;
- Espaço em disco livre e total;
- Temperatura do processador.

Além disso, o sistema realizará uma média simples dos dados de todos os clientes conectados e permitirá a visualização individual de cada cliente em tempo real.

---

### 2. Principais Necessidades dos Usuários

O sistema será utilizado por um único usuário (administrador do servidor), que terá as seguintes necessidades:
- Acesso às informações dos clientes conectados em tempo real;
- Análise estatística simples dos dados coletados;
- Capacidade de enviar comandos aos clientes para executar ações específicas em seus sistemas.

---

### 3. Visão Geral do Sistema

O sistema será composto por:
- **Interface Gráfica**: Desenvolvida com a biblioteca [Streamlit](https://streamlit.io), permitindo a visualização dos dados coletados de maneira intuitiva e dinâmica.
- **Comunicação Cliente-Servidor**: Utilização da biblioteca [Socket](https://docs.python.org/3/library/socket.html) para a troca de informações entre os clientes e o servidor.
- **Armazenamento de Dados**: Os dados coletados serão armazenados em um arquivo ***JSON***, que servirá como um banco de dados leve e acessível.
- **Segurança**: Implementação de criptografia para garantir a segurança na transmissão de dados entre cliente e servidor.
- **Atualização Periódica**: Os clientes enviarão seus dados ao servidor em intervalos de tempo pré-definidos, garantindo informações sempre atualizadas.

---

### 4. Requisitos Funcionais

| Código | Nome | Descrição |
|:---  |:--- |:--- |
| RF01 | Entrar na conta | Visitante acessa a plataforma para fazer login e entrar no sistema. |
| RF02 | Coletar Dados de Hardware | O cliente deve enviar informações sobre processadores, memória RAM, espaço em disco e temperatura do processador ao servidor. |
| RF03 | Exibir Média dos Dados | O sistema deve calcular e exibir a média dos dados coletados de todos os clientes conectados. |
| RF04 | Listar e Detalhar Computadores | O usuário deve conseguir visualizar a lista de computadores conectados e acessar detalhes individuais. |

---

### 5. Requisitos Não-Funcionais

| Código | Nome | Descrição | Categoria | Classificação |
|:---  |:--- |:--- |:--- |:--- |
| RNF01 | Design responsivo | O sistema deve adaptar-se a qualquer tamanho de tela de dispositivo, seja, computador, tablets ou smartphones. | Usabilidade | Obrigatório |
| RNF02 | Uso de Sockets puro | A comunicação entre cliente e servidor deve ser realizada utilizando apenas a biblioteca Socket do Python. | Desempenho | Obrigatório |
| RNF03 | Comunicação Segura | Os dados trocados entre cliente e servidor devem ser criptografados para garantir a segurança das informações. | Segurança | Obrigatório |
| RNF04 | Arquitetura Cliente/Servidor | O sistema deve seguir a arquitetura Cliente/Servidor para garantir escalabilidade e organização. | Arquitetura | Obrigatório |
| RNF05 | Localização Automática dos Clientes | O servidor deve ser capaz de localizar e registrar automaticamente os clientes que se conectam. | Funcionalidade | Obrigatório |
| RNF06 | Desenvolvimento Orientado a Objetos | O sistema deve ser desenvolvido utilizando o paradigma de Programação Orientada a Objetos. | Qualidade de Código | Obrigatório |

---

### 6. Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| Python | Linguagem principal do projeto |
| Streamlit | Interface gráfica do servidor |
| Socket | Comunicação cliente-servidor |
| JSON | Armazenamento dos dados coletados |
| Criptografia | Segurança na transmissão dos dados |



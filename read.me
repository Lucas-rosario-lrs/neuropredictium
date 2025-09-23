# Neuropreditium: Plataforma de Diagnóstico Auxiliar via IoT

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=yellow)
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green?logo=mongodb)
![Arduino](https://img.shields.io/badge/Arduino-C++-00979D?logo=arduino)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

## 📖 Sobre o Projeto

**Neuropreditium** é uma plataforma de prova de conceito (PoC) desenvolvida para coletar e analisar dados biométricos em tempo real, utilizando hardware de baixo custo (Arduino e sensores) para auxiliar na detecção precoce de possíveis indicadores de doenças neurodegenerativas.

O sistema possui duas frentes de análise principais:
1.  **Análise de Tremor:** Utiliza um acelerômetro/giroscópio (MPU-6050) para medir a frequência de tremores em Hertz. Esses dados são então processados por um modelo de Machine Learning (Random Forest) para classificar o tremor.
2.  **Análise de Amostras de Saliva:** Utiliza um sensor de cor (TCS34725) para analisar a colorimetria de amostras de saliva com reagentes, buscando identificar a presença de proteínas oxidadas, que podem ser um biomarcador para doenças como o Alzheimer.

Todos os dados são enviados para um servidor central, armazenados em um banco de dados e exibidos em um dashboard web em tempo real.

## ✨ Funcionalidades

- **Coleta de Dados em Tempo Real:** Captura de dados de frequência de tremor e de cor (RGB, Lux, Temp. Cor) via Arduino.
- **Comunicação Robusta:** Sistema de ponte via script Python para transmitir dados da porta serial para um servidor web.
- **Predição com Machine Learning:** Integração de um modelo `.pkl` (Random Forest) treinado para fornecer um diagnóstico em tempo real com base nos dados de tremor.
- **Persistência de Dados:** Armazenamento de todas as leituras e análises em um banco de dados NoSQL (MongoDB) para futuras consultas e re-treinamento de modelos.
- **Dashboard Web Interativo:** Frontend simples e reativo que exibe os dados coletados e os diagnósticos em tempo real, com atualização automática.

## 🏗️ Arquitetura do Sistema

O fluxo de dados da plataforma foi desenhado de forma modular:

**`Sensor (MPU-6050 / TCS34725)`** → **`Arduino`** → `[USB]` → **`Ponte Python (Serial para HTTP)`** → `[HTTP POST]` → **`Servidor Flask (Python)`** → **`Banco de Dados (MongoDB)`**

O Frontend, por sua vez, consome os dados da seguinte forma:

**`Navegador Web (Frontend)`** ← `[HTTP GET]` ← **`Servidor Flask (Python)`** ← **`Banco de Dados (MongoDB)`**

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologias |
| :--- | :--- |
| **Hardware** | Arduino Uno, Sensor MPU-6050, Sensor TCS34725, Display OLED SSD1306 |
| **Backend** | Python 3, Flask, PyMongo, Scikit-learn, Pandas, NumPy, Flask-CORS |
| **Ponte de Dados** | Python 3, PySerial, Requests |
| **Banco de Dados** | MongoDB |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla JS com Fetch API) |
| **Versionamento** | Git & GitHub |
## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o ambiente completo.

### 1. Pré-requisitos
Certifique-se de ter os seguintes softwares instalados:
- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/)
- [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- [Arduino IDE](https://www.arduino.cc/en/software)

### 2. Clone o Repositório
```bash
git clone [https://github.com/Lucas-rosario-lrs/neuropreditium.git](https://github.com/Lucas-rosario-lrs/neuropreditium.git)
cd neuropreditium

### 3. Config de ambiente
```bash
pip install -r requirements.txt


### 4. Carregar no Arduíno

Carregue arduino/tremor.ino no Arduino de tremor.

Carregue arduino/sensordecor.ino no Arduino de saliva.

Anote as portas COM de cada um. E configure as portas serial em `backend\ponte_serial`

### 5. Executando o Sistema

Você precisará de, no mínimo, 3 terminais abertos.


Terminal 1 (Banco de Dados):

# Inicie o serviço do MongoDB. Se não iniciar automaticamente, use o comando manual:
```bash
"C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe"


Terminal 2 (Servidor Backend):
```bash
cd backend/server
python server.py


Terminal 3 (Ponte de Dados):
```bash
# Conecte o Arduino que você quer testar
cd backend

# Para testar o tremor:
python ponte_tremor.py

# Ou para testar a saliva (em outro momento):
python ponte_saliva.py





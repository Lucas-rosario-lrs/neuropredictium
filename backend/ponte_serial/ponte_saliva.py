import serial
import requests
import json
import time

# --- CONFIGURAÇÃO CRÍTICA ---

PORTA_SERIAL = 'COM6'  

# -------------------------------------------------------------

# A velocidade deve ser a mesma do Serial.begin() no Arduino
VELOCIDADE_SERIAL = 9600

# A URL para onde os dados serão enviados (seu servidor Node.js)
URL_SERVIDOR = 'http://localhost:3000/saliva'


print("[Ponte Python] Tentando iniciar...")
try:
    # Inicia a conexão com a porta serial
    arduino = serial.Serial(PORTA_SERIAL, VELOCIDADE_SERIAL, timeout=2)
    # Espera 2 segundos para a conexão serial se estabilizar
    time.sleep(2) 
    print(f"[Ponte Python] Conectado e ouvindo a porta serial {PORTA_SERIAL}...")

    # Loop infinito para ler os dados continuamente
    while True:
        # Lê uma linha inteira de dados vinda do Arduino (até a quebra de linha)
        linha = arduino.readline().decode('utf-8').strip()

        # Verifica se a linha não está vazia
        if linha:
            print(f"[Ponte Python] Recebido do Arduino: {linha}")
            try:
                # Converte a string JSON em um objeto Python (dicionário)
                dados = json.loads(linha)
                
                # Envia os dados para o servidor local via requisição POST
                resposta = requests.post(URL_SERVIDOR, data=dados)
                
                # Imprime uma confirmação de que os dados foram enviados
                print(f"[Ponte Python] Enviado para o servidor. Status: {resposta.status_code} - {resposta.text}")

            except json.JSONDecodeError:
                print("[Ponte Python] Erro: Dado recebido do Arduino não é um JSON válido.")
            except requests.exceptions.RequestException as e:
                print(f"[Ponte Python] Erro de conexão com o servidor: {e}")
            except Exception as e:
                print(f"[Ponte Python] Ocorreu um erro inesperado: {e}")


except serial.SerialException as e:
    print(f"[Ponte Python] ERRO CRÍTICO: Não foi possível abrir a porta serial '{PORTA_SERIAL}'.")
    print("Por favor, verifique se:")
    print("  1) O nome da porta no script está 100% correto.")
    print("  2) O Arduino está firmemente conectado ao computador.")
    print("  3) O Monitor Serial da IDE do Arduino (ou qualquer outro programa de terminal) está FECHADO.")
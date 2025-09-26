# Arquivo 4: ponte_saliva.py (Corrigido)
import serial, requests, json, time

PORTA_SERIAL = 'COM6'  # <-- ATUALIZE AQUI!
VELOCIDADE_SERIAL = 9600
# --- MUDANÇA CRÍTICA: A porta agora é 5000 ---
URL_SERVIDOR = 'http://localhost:5000/api/saliva'

print("[Ponte Python - Saliva] Tentando iniciar...")
try:
    arduino = serial.Serial(PORTA_SERIAL, VELOCIDADE_SERIAL, timeout=2)
    time.sleep(2) 
    print(f"[Ponte Python - Saliva] Conectado e ouvindo a porta serial {PORTA_SERIAL}...")
    while True:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"[Ponte Python - Saliva] Recebido: {linha}")
            try:
                dados = json.loads(linha)
                resposta = requests.post(URL_SERVIDOR, data=dados)
                print(f"[Ponte Python - Saliva] Enviado. Status: {resposta.status_code}")
            except Exception as e:
                print(f"[Ponte Python - Saliva] Ocorreu um erro: {e}")
except serial.SerialException:
    print(f"\n[Ponte Python - Saliva] ERRO CRÍTICO: Não foi possível abrir a porta serial '{PORTA_SERIAL}'.")
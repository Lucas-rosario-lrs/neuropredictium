from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import joblib
import numpy as np
import os

# --- Configuração Inicial ---
app = Flask(__name__, template_folder='../../frontend', static_folder='../../frontend')
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['diagnostico_db']
collection_tremor = db['leituras_tremor']
collection_saliva = db['analises_saliva']

# --- Carregando o Modelo de IA ---
# Este modelo agora deve ser treinado para receber TODOS os parâmetros juntos
modelo_completo = None
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    caminho_do_modelo = os.path.join(backend_dir, 'ml_IA', 'modelo_pipeline.pkl') # << Nome do modelo
    with open(caminho_do_modelo, 'rb') as f:
        modelo_completo = joblib.load(f)
    print(f"[Servidor] Modelo de predição completo carregado de: {caminho_do_modelo}")
except Exception as e:
    print(f"[Servidor] AVISO: Não foi possível carregar o modelo de predição completo: {e}")

# ==========================================================
# --- ROTAS DE COLETA DE DADOS ---
# ==========================================================

@app.route('/api/tremor', methods=['POST'])
def receber_dados_tremor():
    dados = request.form
    try:
        frequencia = float(dados['frequencia'])
        novo_dado = {'frequencia': frequencia, 'timestamp': datetime.utcnow()}
        collection_tremor.insert_one(novo_dado)
        print(f"[Servidor] Dado de tremor recebido e salvo: {frequencia} Hz")
        return jsonify({'status': 'sucesso'}), 201
    except (KeyError, ValueError):
        return jsonify({'erro': 'Dado "frequencia" ausente ou inválido'}), 400

@app.route('/api/saliva', methods=['POST'])
def receber_dados_saliva():
    dados = request.form
    try:
        nova_analise = {
            'readings': { 'r': int(dados['r']), 'g': int(dados['g']), 'b': int(dados['b']), 'c': int(dados['c']), 'lux': int(dados['lux']), 'tempCor': int(dados['tempCor']) },
            'analysisResult': dados['corDetectada'], 'timestamp': datetime.utcnow()
        }
        collection_saliva.insert_one(nova_analise)
        print(f"[Servidor] Amostra de saliva recebida e salva.")
        return jsonify({'status': 'sucesso'}), 201
    except (KeyError, ValueError):
        return jsonify({'erro': 'Dados da amostra de saliva incompletos ou malformados'}), 400

# ==========================================================
# --- ROTA DE ANÁLISE COMPLETA 
# ==========================================================
@app.route('/api/analise_completa', methods=['POST'])
def fazer_analise_completa():
    if not modelo_completo:
        return jsonify({'erro': 'Modelo de predição não está disponível'}), 500

    # 1. Buscar os dados mais recentes de cada fonte no banco de dados
    ultimo_tremor = collection_tremor.find_one({}, sort=[('timestamp', -1)])
    ultima_saliva = collection_saliva.find_one({}, sort=[('timestamp', -1)])

    if not ultimo_tremor or not ultima_saliva:
        return jsonify({'erro': 'Dados insuficientes. É preciso ter ao menos uma leitura de tremor e uma de saliva.'}), 404

    # 2. Montando pacote de dados para o modelo
    # 
    try:
        dados_para_predicao = np.array([[
            ultima_saliva['readings']['r'],
            ultima_saliva['readings']['g'],
            ultima_saliva['readings']['b'],
            ultimo_tremor['frequencia']
            # ADICIONE MAIS PARÂMETROS AQUI
        ]])
        
        print(f"[Servidor] Realizando predição com os dados combinados: {dados_para_predicao}")

        # 3. Fazer a predição
        predicao_array = modelo_completo.predict(dados_para_predicao)
        probabilidade = modelo_completo.predict_proba(dados_para_predicao)
        diagnostico = str(predicao_array[0])
        confianca = f"{np.max(probabilidade) * 100:.2f}%"

        return jsonify({'diagnostico_completo': diagnostico, 'confianca': confianca})

    except Exception as e:
        print(f"[Servidor] Erro durante a predição completa: {e}")
        return jsonify({'erro': 'Erro interno ao processar a predição'}), 500


# ROTAS DO FRONTEND
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/tremores_data', methods=['GET'])
def get_tremores_data():
    return jsonify(list(collection_tremor.find({}, {'_id': 0}).sort('timestamp', -1).limit(10)))
@app.route('/api/saliva_data', methods=['GET'])
def get_saliva_data():
    return jsonify(list(collection_saliva.find({}, {'_id': 0}).sort('timestamp', -1).limit(10)))

if __name__ == '__main__':
    print("[Servidor] Iniciando o servidor de diagnóstico unificado...")
    app.run(host='0.0.0.0', port=5000, debug=True)
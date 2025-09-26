# Arquivo 2: server.py (Versão Final)
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import joblib
import numpy as np
import os

app = Flask(__name__, template_folder='../../frontend', static_folder='../../frontend')
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['diagnostico_db']
collection_tremor = db['leituras_tremor']
collection_saliva = db['analises_saliva']

modelo_tremor = None
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    # --- MUDANÇA CRÍTICA: Carregando o modelo da pipeline ---
    caminho_do_modelo = os.path.join(backend_dir, 'ml_IA', 'modelo_pipeline.pkl')
    
    print(f"[Servidor] Procurando modelo em: {caminho_do_modelo}")
    with open(caminho_do_modelo, 'rb') as f:
        modelo_tremor = joblib.load(f)
    print("[Servidor] Modelo de predição (modelo_pipeline.pkl) carregado com sucesso.")
except Exception as e:
    print(f"[Servidor] ERRO ao carregar modelo: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tremores_data', methods=['GET'])
def get_tremores_data():
    leituras = list(collection_tremor.find({}, {'_id': 0}).sort('timestamp', -1).limit(10))
    return jsonify(leituras)

@app.route('/api/saliva_data', methods=['GET'])
def get_saliva_data():
    analises = list(collection_saliva.find({}, {'_id': 0}).sort('timestamp', -1).limit(10))
    return jsonify(analises)

@app.route('/api/tremor', methods=['POST'])
def receber_dados_tremor():
    dados = request.form
    try:
        frequencia = float(dados['frequencia'])
    except (KeyError, ValueError):
        return jsonify({'erro': 'Dado "frequencia" ausente ou inválido'}), 400

    print(f"[Servidor] Leitura de TREMOR recebida: {frequencia} Hz")
    diagnostico, confianca = "Modelo não disponível", "0.00%"
    if modelo_tremor:
        dados_para_predicao = np.array([[frequencia]])
        predicao_array = modelo_tremor.predict(dados_para_predicao)
        probabilidade = modelo_tremor.predict_proba(dados_para_predicao)
        diagnostico = str(predicao_array[0])
        confianca = f"{np.max(probabilidade) * 100:.2f}%"
        print(f"[Servidor] Predição de Tremor: {diagnostico} com {confianca} de confiança.")

    novo_dado_tremor = {'frequencia': frequencia, 'diagnostico': diagnostico, 'confianca': confianca, 'timestamp': datetime.utcnow()}
    collection_tremor.insert_one(novo_dado_tremor)
    return jsonify({'status': 'sucesso', 'diagnostico_tremor': diagnostico}), 201

@app.route('/api/saliva', methods=['POST'])
def receber_dados_saliva():
    dados = request.form
    try:
        nova_analise = {
            'readings': { 'r': int(dados['r']), 'g': int(dados['g']), 'b': int(dados['b']), 'c': int(dados['c']), 'lux': int(dados['lux']), 'tempCor': int(dados['tempCor']) },
            'analysisResult': dados['corDetectada'], 'timestamp': datetime.utcnow()
        }
    except (KeyError, ValueError): return jsonify({'erro': 'Dados da amostra de saliva incompletos ou malformados'}), 400
    collection_saliva.insert_one(nova_analise)
    return jsonify({'status': 'sucesso', 'message': 'Amostra de saliva salva com sucesso'}), 201

if __name__ == '__main__':
    print("[Servidor] Iniciando o servidor de diagnóstico...")
    app.run(host='0.0.0.0', port=5000, debug=True)
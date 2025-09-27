import joblib
import pandas as pd
import numpy as np
from tabulate import tabulate
from sklearn.metrics import classification_report, accuracy_score

# === CONFIGURAÇÕES ===
arquivo_modelo = "modelo_pipeline.pkl"  # substitua pelo seu modelo salvo
arquivo_csv = "fake_neuro_dataset_rgb_freq_501.csv"

# === CARREGA MODELO ===
with open(arquivo_modelo, "rb") as f:
    modelo = joblib.load(f)

# === CARREGA DADOS DE TESTE ===
dados = pd.read_csv(arquivo_csv)
X_teste = dados.drop(columns=["label"])
y_teste = dados["label"]

# === PREDIÇÃO ===
predicoes = modelo.predict(X_teste)
probabilidades = modelo.predict_proba(X_teste)

# === PREPARA TABELA ===
classes_modelo = modelo.classes_

linhas = []
for i in range(len(X_teste)):
    esperado = y_teste.iloc[i]
    predito = predicoes[i]
    probs = probabilidades[i]
    linha = [esperado, predito] + list(np.round(probs, 3))
    linhas.append(linha)

cabecalho = ["Classe Esperada", "Classe Predita"] + [f"Prob({c})" for c in classes_modelo]

# === MOSTRA RESULTADOS ===
print("Predições do modelo para o dataset de teste (30 amostras):\n")
print(tabulate(linhas, headers=cabecalho, tablefmt="grid"))

# === MÉTRICAS GLOBAIS ===
print("\nMétricas gerais no dataset de teste:")
print(f"Acurácia: {accuracy_score(y_teste, predicoes):.4f}")
print(classification_report(y_teste, predicoes))
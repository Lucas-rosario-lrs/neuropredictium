import joblib
import pandas as pd
import numpy as np
from tabulate import tabulate

# === CONFIGURAÇÕES ===
arquivo_modelo = "modelo_pipeline.pkl"  # substitua pelo seu modelo salvo
arquivo_csv = "fake_neuro_dataset_teste.csv"

# === CARREGA MODELO ===
with open(arquivo_modelo, "rb") as f:
    modelo = joblib.load(f)

# === CARREGA DADOS DE TESTE ===
dados = pd.read_csv(arquivo_csv)
X_teste = dados.drop(columns=["label"])
y_teste = dados["label"]

# === NORMALIZAÇÃO (caso tenha usado scaler no pipeline) ===
# Se você salvou o scaler separadamente, carregue e transforme:
# from joblib import load
# scaler = load("scaler.pkl")
# X_teste = scaler.transform(X_teste)

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

# === MOSTRA RESULTADO ===
print("Predições do modelo para o novo dataset de teste (30 amostras):\n")
print(tabulate(linhas, headers=cabecalho, tablefmt="grid"))
import joblib
import pandas as pd
import numpy as np

# ===============================
# 1. Carregar modelo e scaler
# ===============================
modelo = joblib.load("modelo_rf.pkl")
scaler = joblib.load("scaler.pkl")

# ===============================
# 2. Colunas esperadas pelo scaler
# ===============================
colunas = ["conc_alpha_syn","R","G","B","Clear","tremor_peak_freq","tremor_band_power","tremor_rms"]

# ===============================
# 3. Entradas de teste ajustadas
# Valores inspirados nos intervalos que usamos para gerar cada classe no CSV sintético
# ===============================
entradas = {
    "Saudável": [0.2, 105, 110, 115, 200, 2.0, 0.05, 0.01],
    "Parkinson": [0.6, 120, 115, 110, 220, 6.0, 0.8, 0.05],
    "Alzheimer": [1.0, 130, 125, 120, 240, 4.0, 0.5, 0.03]
}

# ===============================
# 4. Preparar DataFrame para scaler
# ===============================
df_test = pd.DataFrame.from_dict(entradas, orient="index", columns=colunas)

# ===============================
# 5. Pré-processar e prever
# ===============================
df_scaled = scaler.transform(df_test)
predicoes = modelo.predict(df_scaled)
probabilidades = modelo.predict_proba(df_scaled)

# ===============================
# 6. Mostrar resultados em tabela
# ===============================
resultado = pd.DataFrame({
    "Classe Esperada": list(entradas.keys()),
    "Classe Predita": predicoes
})

# Adiciona probabilidades
for i, classe_modelo in enumerate(modelo.classes_):
    resultado[f"Prob_{classe_modelo}"] = probabilidades[:, i]

print("\n=== Resultado do teste do modelo ===")
print(resultado.to_string(index=False))
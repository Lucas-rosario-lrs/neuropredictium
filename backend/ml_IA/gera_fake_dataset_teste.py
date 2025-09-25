#*-*coding:latin-1-*-
import pandas as pd
import numpy as np

# Número de amostras por classe
n_por_classe = 10

# --- Função para gerar amostras ---
def gerar_amostras(classe):
    amostras = []
    for _ in range(n_por_classe):
        if classe == "Normal":
            conc_alpha_syn = np.random.uniform(0, 0.05)
            R = np.random.randint(807, 811)
            G = np.random.randint(853, 857)
            B = np.random.randint(720, 724)
            Clear = np.random.randint(2430, 2440)
            tremor_peak_freq = np.random.uniform(0.5, 3)  # tremor muito baixo
            tremor_band_power = np.random.uniform(0, 0.1)
            tremor_rms = np.random.uniform(0, 0.1)
        elif classe == "Parkinson":
            conc_alpha_syn = np.random.uniform(0.3, 0.5)
            R = np.random.randint(750, 810)
            G = np.random.randint(780, 860)
            B = np.random.randint(650, 730)
            Clear = np.random.randint(2200, 2440)
            tremor_peak_freq = np.random.uniform(4, 6)  # banda típica Parkinson
            tremor_band_power = np.random.uniform(0.5, 1.0)
            tremor_rms = np.random.uniform(0.5, 1.0)
        elif classe == "Alzheimer":
            conc_alpha_syn = np.random.uniform(0, 0.1)
            R = np.random.randint(424, 591)
            G = np.random.randint(360, 566)
            B = np.random.randint(301, 460)
            Clear = np.random.randint(1115, 1667)
            tremor_peak_freq = np.random.uniform(0.5, 3)  # tremor baixo ou normal
            tremor_band_power = np.random.uniform(0, 0.2)
            tremor_rms = np.random.uniform(0, 0.2)
        amostras.append([conc_alpha_syn, R, G, B, Clear, tremor_peak_freq, tremor_band_power, tremor_rms, classe])
    return amostras

# --- Gerar todas as amostras ---
dataset = []
for c in ["Normal", "Parkinson", "Alzheimer"]:
    dataset.extend(gerar_amostras(c))

# --- Criar DataFrame e salvar CSV ---
colunas = ["conc_alpha_syn","R","G","B","Clear","tremor_peak_freq","tremor_band_power","tremor_rms","label"]
df_teste = pd.DataFrame(dataset, columns=colunas)
df_teste.to_csv("fake_neuro_dataset_teste.csv", index=False)

print("Dataset de teste gerado com sucesso: fake_neuro_dataset_teste.csv")

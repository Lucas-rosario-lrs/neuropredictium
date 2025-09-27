# gera_fake_dataset_teste_rgb_freq.py
import pandas as pd
import numpy as np

# Fixar semente para reprodutibilidade
np.random.seed(123)

# Quantidade por classe
n = 10  

def gerar_normal(n):
    r = np.random.normal(808, 30, n).astype(int)
    g = np.random.normal(855, 30, n).astype(int)
    b = np.random.normal(722, 30, n).astype(int)
    freq = np.random.uniform(1.0, 2.0, n)
    return pd.DataFrame({"r": r, "g": g, "b": b, "frequency": freq, "label": "Normal"})

def gerar_parkinson(n):
    r = np.random.normal(605, 30, n).astype(int)
    g = np.random.normal(655, 30, n).astype(int)
    b = np.random.normal(520, 30, n).astype(int)
    freq = np.random.uniform(4.0, 6.0, n)
    return pd.DataFrame({"r": r, "g": g, "b": b, "frequency": freq, "label": "Parkinson"})

def gerar_alzheimer(n):
    r = np.random.normal(500, 40, n).astype(int)
    g = np.random.normal(450, 40, n).astype(int)
    b = np.random.normal(400, 40, n).astype(int)
    freq = np.random.uniform(1.0, 6.0, n)
    return pd.DataFrame({"r": r, "g": g, "b": b, "frequency": freq, "label": "Alzheimer"})

def main():
    df_normal = gerar_normal(n)
    df_parkinson = gerar_parkinson(n)
    df_alzheimer = gerar_alzheimer(n)

    df_final = pd.concat([df_normal, df_parkinson, df_alzheimer], ignore_index=True)
    df_final = df_final.sample(frac=1, random_state=123).reset_index(drop=True)

    caminho = "fake_neuro_dataset_teste_rgb_freq.csv"
    df_final.to_csv(caminho, index=False)
    print(f"Dataset de teste salvo em {caminho} com {len(df_final)} amostras.")
    print(df_final.head())

if __name__ == "__main__":
    main()
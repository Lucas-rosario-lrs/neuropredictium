import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ============================================================
# 1. Carregamento do dataset
# ============================================================
def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Carrega o dataset CSV para um DataFrame pandas."""
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo {caminho_csv} não encontrado.")
    return pd.read_csv(caminho_csv)


# ========================================================================
# 2. Pré-processamento
# =======================================================================
def preprocessar_dados(df: pd.DataFrame, target_col: str):
    """
    Divide em features e rótulos, faz split em treino/teste e normaliza.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


# ============================================================
# 3. Treinamento do modelo
# ============================================================
def treinar_modelo(X_train, y_train, n_estimators=200, random_state=42):
    """
    Treina um modelo Random Forest.
    """
    modelo = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        class_weight="balanced"
    )
    modelo.fit(X_train, y_train)
    return modelo


# ============================================================
# 4. Avaliação do modelo
# ============================================================
def avaliar_modelo(modelo, X_test, y_test):
    """
    Avalia o modelo no conjunto de teste.
    """
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    relatorio = classification_report(y_test, y_pred)
    print(f"Acurácia: {acc:.4f}")
    print("Relatório de Classificação:\n", relatorio)


# ============================================================
# 5. Persistência do modelo
# ============================================================
def salvar_modelo(modelo, scaler, caminho_modelo="modelo_rf.pkl", caminho_scaler="scaler.pkl"):
    """Salva modelo e scaler para uso posterior."""
    joblib.dump(modelo, caminho_modelo)
    joblib.dump(scaler, caminho_scaler)
    print(f"Modelo salvo em {caminho_modelo}")
    print(f"Scaler salvo em {caminho_scaler}")


def carregar_modelo(caminho_modelo="modelo_rf.pkl", caminho_scaler="scaler.pkl"):
    """Carrega modelo e scaler previamente salvos."""
    if not os.path.exists(caminho_modelo) or not os.path.exists(caminho_scaler):
        raise FileNotFoundError("Modelo ou scaler não encontrados.")
    modelo = joblib.load(caminho_modelo)
    scaler = joblib.load(caminho_scaler)
    return modelo, scaler


# ============================================================
# 6. Função principal
# ============================================================
def main():
    # Caminho do dataset
    caminho_csv = "fake_neuro_dataset.csv"
    target_col = "label"  # ajuste conforme seu dataset

    # 1. Carregar dados
    df = carregar_dados(caminho_csv)

    # 2. Pré-processar
    X_train, X_test, y_train, y_test, scaler = preprocessar_dados(df, target_col)

    # 3. Treinar
    modelo = treinar_modelo(X_train, y_train)

    # 4. Avaliar
    avaliar_modelo(modelo, X_test, y_test)

    # 5. Salvar
    salvar_modelo(modelo, scaler)


if __name__ == "__main__":
    main()
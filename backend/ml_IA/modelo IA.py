import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import joblib

def main():
    caminho_csv = "fake_neuro_dataset.csv"
    target_col = "label"

    df = pd.read_csv(caminho_csv)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Pipeline com scaler + modelo
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("Acurácia:", accuracy_score(y_test, y_pred))
    print("Relatório:\n", classification_report(y_test, y_pred))

    joblib.dump(pipeline, "modelo_pipeline.pkl")
    print("Modelo salvo em modelo_pipeline.pkl")

if __name__ == "__main__":
    main()
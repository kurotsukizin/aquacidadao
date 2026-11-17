from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split

RAIZ = Path(__file__).resolve().parents[1]
TRATADO = RAIZ / "data" / "consumo_tratado.csv"
RESULTADO = RAIZ / "evidencias" / "resultados_modelo.txt"


def main():
    df = pd.read_csv(TRATADO)

    X = pd.get_dummies(
        df[[
            "vazao_l_min", "volume_litros", "hora",
            "horario", "ponto_de_uso", "media_movel_6h"
        ]],
        columns=["horario", "ponto_de_uso"]
    )

    y = df["risco"]

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    modelo = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    modelo.fit(X_treino, y_treino)
    previsoes = modelo.predict(X_teste)

    relatorio = f"""AQUACIDADAO - AVALIACAO DO MODELO

Modelo: RandomForestClassifier
Registros de treino: {len(X_treino)}
Registros de teste: {len(X_teste)}

Acuracia: {accuracy_score(y_teste, previsoes):.4f}
Acuracia balanceada: {balanced_accuracy_score(y_teste, previsoes):.4f}
F1-score macro: {f1_score(y_teste, previsoes, average='macro'):.4f}

Relatorio de classificacao:
{classification_report(y_teste, previsoes)}

Matriz de confusao:
{confusion_matrix(y_teste, previsoes)}

Limitacoes:
- Base simulada e balanceada artificialmente para demonstrar alertas.
- O modelo apoia a triagem, mas nao confirma vazamentos.
"""

    RESULTADO.write_text(relatorio, encoding="utf-8")
    print(relatorio)


if __name__ == "__main__":
    main()

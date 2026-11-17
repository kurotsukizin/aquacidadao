from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RAIZ = Path(__file__).resolve().parents[1]
TRATADO = RAIZ / "data" / "consumo_tratado.csv"
RESUMO = RAIZ / "data" / "resumo_diario.csv"
IMAGENS = RAIZ / "images"

IMAGENS.mkdir(exist_ok=True)


def main():
    df = pd.read_csv(TRATADO, parse_dates=["data_hora"])
    resumo = pd.read_csv(RESUMO)

    plt.figure(figsize=(14, 5))
    diario = df.groupby(df["data_hora"].dt.date)["volume_litros"].sum()
    diario.plot(kind="line", marker="o", color="#1976D2")
    plt.title("Consumo diario de agua")
    plt.xlabel("Data")
    plt.ylabel("Litros consumidos")
    plt.tight_layout()
    plt.savefig(IMAGENS / "01_consumo_diario.png", dpi=150)
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x="horario", y="volume_litros", estimator=sum, errorbar=None, palette="Blues", hue="horario", legend=False)
    plt.title("Consumo por periodo do dia")
    plt.xlabel("Periodo")
    plt.ylabel("Litros")
    plt.tight_layout()
    plt.savefig(IMAGENS / "02_consumo_por_horario.png", dpi=150)
    plt.show()

    plt.figure(figsize=(10, 5))
    contagem = df["risco"].value_counts()
    contagem.plot(kind="bar", color=["#66BB6A", "#FFB300", "#E53935"])
    plt.title("Classificacao de risco dos registros")
    plt.xlabel("Risco")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.savefig(IMAGENS / "03_alertas_por_dia.png", dpi=150)
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.histplot(df["volume_litros"], bins=30, kde=True, color="#1976D2")
    plt.title("Distribuicao do volume consumido")
    plt.xlabel("Litros")
    plt.ylabel("Frequencia")
    plt.tight_layout()
    plt.savefig(IMAGENS / "04_distribuicao_consumo.png", dpi=150)
    plt.show()

    print(resumo.tail(10))


if __name__ == "__main__":
    main()

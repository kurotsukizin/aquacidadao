from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTO = RAIZ / "data" / "consumo_bruto.csv"
TRATADO = RAIZ / "data" / "consumo_tratado.csv"
RESUMO = RAIZ / "data" / "resumo_diario.csv"
RELATORIO = RAIZ / "evidencias" / "relatorio_tratamento.txt"


def classificar_risco(volume, media, desvio):
    limite_atencao = media + desvio
    limite_desperdicio = media + 2 * desvio

    if volume > limite_desperdicio:
        return "possivel_desperdicio"

    if volume > limite_atencao:
        return "atencao"

    return "normal"


def main():
    if not BRUTO.exists():
        raise FileNotFoundError("Execute primeiro src/gerar_base.py")

    df = pd.read_csv(BRUTO)
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df["data"] = df["data_hora"].dt.date
    df["hora"] = df["data_hora"].dt.hour

    estatisticas = df.groupby("ponto_de_uso")["volume_litros"].agg(["mean", "std"])

    riscos = []
    for linha in df.itertuples(index=False):
        media = estatisticas.loc[linha.ponto_de_uso, "mean"]
        desvio = estatisticas.loc[linha.ponto_de_uso, "std"]
        riscos.append(classificar_risco(linha.volume_litros, media, desvio))

    df["risco"] = riscos
    df["media_movel_6h"] = df["volume_litros"].rolling(6, min_periods=1).mean().round(3)

    df.to_csv(TRATADO, index=False)

    resumo = df.groupby("data").agg(
        total_registros=("volume_litros", "size"),
        volume_total_litros=("volume_litros", "sum"),
        volume_medio=("volume_litros", "mean"),
        volume_maximo=("volume_litros", "max"),
        alertas_atencao=("risco", lambda x: (x == "atencao").sum()),
        alertas_desperdicio=("risco", lambda x: (x == "possivel_desperdicio").sum())
    ).round(2)

    resumo.to_csv(RESUMO)

    atencao = int((df["risco"] == "atencao").sum())
    desperdicio = int((df["risco"] == "possivel_desperdicio").sum())

    relatorio = f"""AQUACIDADAO - RELATORIO DE TRATAMENTO

Registros recebidos: {len(df)}
Registros tratados: {len(df)}
Periodo: {df['data_hora'].min()} a {df['data_hora'].max()}
Volume total: {df['volume_litros'].sum():.2f} litros
Volume medio por registro: {df['volume_litros'].mean():.2f} litros

Alertas de atencao: {atencao}
Alertas de possivel desperdicio: {desperdicio}

Observacoes:
- Base de demonstracao gerada pelo projeto.
- O risco e calculado a partir da media e do desvio-padrao por ponto de uso.
- O resultado nao confirma tecnicamente um vazamento.
"""

    RELATORIO.parent.mkdir(parents=True, exist_ok=True)
    RELATORIO.write_text(relatorio, encoding="utf-8")

    print(f"Arquivo tratado: {TRATADO}")
    print(f"Resumo diario: {RESUMO}")
    print(f"Relatorio: {RELATORIO}")


if __name__ == "__main__":
    main()

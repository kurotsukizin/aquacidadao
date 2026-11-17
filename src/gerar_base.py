import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO = RAIZ / "data" / "consumo_bruto.csv"

PONTOS = ["pia_cozinha", "chuveiro", "torneira_banheiro", "irrigacao"]


def gerar_consumo(hora, ponto):
    if ponto == "chuveiro":
        base = 14 if 6 <= hora <= 9 or 18 <= hora <= 22 else 2
    elif ponto == "pia_cozinha":
        base = 8 if 7 <= hora <= 9 or 18 <= hora <= 21 else 2
    elif ponto == "torneira_banheiro":
        base = 5 if 6 <= hora <= 9 or 18 <= hora <= 22 else 1
    else:
        base = 6 if 6 <= hora <= 8 else 0

    return round(max(0, base + random.uniform(-1.5, 1.5)), 2)


def main():
    random.seed(42)
    inicio = datetime(2026, 11, 1, 0, 0, 0)
    registros = []

    for dia in range(30):
        for hora in range(24):
            for ponto in PONTOS:
                vazao = gerar_consumo(hora, ponto)

                if dia >= 25 and ponto == "torneira_banheiro" and 2 <= hora <= 5:
                    vazao = round(random.uniform(8, 14), 2)

                if hora < 6:
                    periodo = "madrugada"
                elif hora < 12:
                    periodo = "manha"
                elif hora < 18:
                    periodo = "tarde"
                else:
                    periodo = "noite"

                registros.append({
                    "data_hora": (inicio + timedelta(days=dia, hours=hora)).strftime("%Y-%m-%d %H:%M:%S"),
                    "local": "Residencia A",
                    "vazao_l_min": vazao,
                    "volume_litros": vazao,
                    "horario": periodo,
                    "ponto_de_uso": ponto,
                    "origem": "simulado"
                })

    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)

    with ARQUIVO.open("w", encoding="utf-8", newline="") as arquivo:
        campos = ["data_hora", "local", "vazao_l_min", "volume_litros", "horario", "ponto_de_uso", "origem"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)

    print(f"Base gerada: {ARQUIVO}")
    print(f"Total de registros: {len(registros)}")


if __name__ == "__main__":
    main()

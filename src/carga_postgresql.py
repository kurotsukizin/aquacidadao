import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
CSV = RAIZ / "data" / "consumo_tratado.csv"


def main():
    load_dotenv(RAIZ / ".env")

    config = {
        "host": os.getenv("PGHOST", "localhost"),
        "port": os.getenv("PGPORT", "5432"),
        "dbname": os.getenv("PGDATABASE"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
    }

    if not all([config["dbname"], config["user"], config["password"]]):
        raise ValueError("Preencha PGDATABASE, PGUSER e PGPASSWORD no .env")

    df = pd.read_csv(CSV)
    df["data_hora"] = pd.to_datetime(df["data_hora"])

    sql = """
        INSERT INTO consumo_agua (
            data_hora, local, vazao_l_min, volume_litros,
            horario, ponto_de_uso, risco, media_movel_6h, origem
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (local, data_hora, ponto_de_uso)
        DO UPDATE SET
            vazao_l_min = EXCLUDED.vazao_l_min,
            volume_litros = EXCLUDED.volume_litros,
            horario = EXCLUDED.horario,
            risco = EXCLUDED.risco,
            media_movel_6h = EXCLUDED.media_movel_6h,
            origem = EXCLUDED.origem;
    """

    with psycopg.connect(**config) as conexao:
        with conexao.cursor() as cursor:
            for linha in df.itertuples(index=False):
                cursor.execute(sql, (
                    linha.data_hora, linha.local, linha.vazao_l_min,
                    linha.volume_litros, linha.horario, linha.ponto_de_uso,
                    linha.risco, linha.media_movel_6h, linha.origem
                ))
        conexao.commit()

    print(f"Carga concluida: {len(df)} registros processados.")


if __name__ == "__main__":
    main()

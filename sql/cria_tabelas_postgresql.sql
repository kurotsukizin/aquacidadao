BEGIN;

CREATE TABLE consumo_agua (
    id_consumo BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    local VARCHAR(100) NOT NULL,
    vazao_l_min NUMERIC(8,2) NOT NULL CHECK (vazao_l_min >= 0),
    volume_litros NUMERIC(8,2) NOT NULL CHECK (volume_litros >= 0),
    horario VARCHAR(20) NOT NULL,
    ponto_de_uso VARCHAR(50) NOT NULL,
    risco VARCHAR(30) NOT NULL CHECK (risco IN ('normal', 'atencao', 'possivel_desperdicio')),
    media_movel_6h NUMERIC(10,3),
    origem VARCHAR(20) NOT NULL,
    data_carga TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_consumo UNIQUE (local, data_hora, ponto_de_uso)
);

COMMIT;

SELECT
    DATE(data_hora) AS data,
    SUM(volume_litros) AS volume_total,
    ROUND(AVG(volume_litros), 2) AS volume_medio,
    COUNT(*) FILTER (WHERE risco = 'atencao') AS alertas_atencao,
    COUNT(*) FILTER (WHERE risco = 'possivel_desperdicio') AS alertas_desperdicio
FROM consumo_agua
GROUP BY DATE(data_hora)
ORDER BY data;

SELECT
    ponto_de_uso,
    SUM(volume_litros) AS volume_total,
    ROUND(AVG(volume_litros), 2) AS volume_medio,
    COUNT(*) FILTER (WHERE risco <> 'normal') AS alertas
FROM consumo_agua
GROUP BY ponto_de_uso
ORDER BY volume_total DESC;

SELECT
    data_hora,
    ponto_de_uso,
    vazao_l_min,
    volume_litros,
    risco
FROM consumo_agua
WHERE risco <> 'normal'
ORDER BY data_hora;

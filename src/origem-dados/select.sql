SELECT
    DATE(created_at)  AS data,
    tipo,
    nome_tipo,
    COUNT(*)          AS quantidade
FROM dados_finais
GROUP BY
    DATE(created_at),
    tipo,
    nome_tipo
ORDER BY
    data,
    tipo;
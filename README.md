# AquaCidadao - CitizenTech 2026.2

POC de monitoramento e alerta de possivel desperdicio de agua em residencias e espacos comunitarios.

## Integrantes

- Guilherme Cabral Mendes Mariano | 574221

## Problema

Muitas residencias e comunidades nao acompanham o consumo de agua em tempo habil. Vazamentos, torneiras abertas e consumo fora do padrao podem gerar desperdicio e custos elevados.

## Solucao

O AquaCidadao coleta registros de consumo, calcula indicadores estatisticos, identifica periodos com consumo anormal e classifica o risco como:

- normal
- atencao
- possivel_desperdicio

A POC utiliza uma base de demonstracao gerada pelo proprio projeto, alem de um prototipo no Wokwi com ESP32 e sensor de fluxo.

## Publico beneficiado

- Moradores de residencias
- Condominios
- Escolas e centros comunitarios
- Hortas urbanas e comunidades rurais

## ODS

- ODS 6 - Agua potavel e saneamento
- ODS 11 - Cidades e comunidades sustentaveis
- ODS 12 - Consumo e producao responsaveis

## Estrutura

```text
aquacidadao/
├── data/
├── docs/
├── evidencias/
├── images/
├── sql/
├── src/
├── video/
└── wokwi/
```

## Execucao

```bash
pip install -r requirements.txt
python src/gerar_base.py
python src/tratamento_dados.py
python src/analise_consumo.py
python src/modelo_risco.py
python src/carga_postgresql.py
```

## Banco de dados

Configure o arquivo `.env`:

```env
PGHOST=localhost
PGPORT=5432
PGDATABASE=aquacidadao
PGUSER=aqua_app
PGPASSWORD=sua_senha
```

Crie as tabelas executando:

```text
sql/cria_tabelas_postgresql.sql
```

## Limitacoes

- A base e simulada e identificada como demonstracao.
- O sensor de fluxo no Wokwi representa o funcionamento, mas nao mede agua real.
- O modelo nao substitui vistoria tecnica para confirmar vazamentos.
- A POC nao realiza cobranca, bloqueio de agua ou intervencao automatica.

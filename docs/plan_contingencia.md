# Plan de Contingencia - API Mercado Libre

## Escenario A: Conexión exitosa con API de ML
- Se implementa OAuth 2.0 con FastAPI.
- Se obtienen datos reales de una cuenta sandbox.
- Los datos se almacenan en las tablas correspondientes por cliente.
- Metabase muestra datos en vivo.

## Escenario B: No hay tiempo o falla la integración con API
- Se utiliza un dataset de contingencia en formato CSV.
- Gabriela prepara los CSV con datos realistas.
- Kelvys ejecuta `scripts/etl/cargar_datos_contingencia.py` para insertar en PostgreSQL.
- Se documenta explícitamente que el sistema está diseñado para recibir la API.

## Dataset de Contingencia
| Archivo CSV | Tabla Destino | Registros |
|---|---|---|
| `clientes_mock.csv` | `clientes` (maestra) | 3 clientes |
| `publicaciones_mock.csv` | `metricas_publicaciones` | 50 por cliente |
| `ventas_mock.csv` | `metricas_costos` | 200 por cliente |
| `reputacion_mock.csv` | `metricas_reputacion` | 6 meses |
| `envios_mock.csv` | `metricas_envios` | 200 por cliente |
| `stock_mock.csv` | `metricas_stock` | 50 por cliente |

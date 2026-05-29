# Plan de Contingencia - API Mercado Libre

## Escenario A: Conexion exitosa con API de ML
- Se implementa OAuth 2.0 con FastAPI.
- Se obtienen datos reales de una cuenta sandbox.
- Los datos se almacenan en las tablas correspondientes por cliente.
- Metabase (http://localhost:3000) muestra datos en vivo.

## Escenario B: No hay tiempo o falla la integracion con API
- Se utiliza un dataset de contingencia en formato CSV.
- Se preparan los CSV con datos realistas.
- Se ejecuta `scripts/etl/carga_datos.py` para insertar en PostgreSQL local.
- Se documenta explicitamente que el sistema esta disenado para recibir la API.

## Dataset de Contingencia
| Archivo CSV | Tabla Destino | Registros |
|---|---|---|
| `clientes_mock.csv` | `clientes` (maestra) | 3 clientes |
| `publicaciones_mock.csv` | `metricas_publicaciones` | 50 por cliente |
| `ventas_mock.csv` | `metricas_costos` | 200 por cliente |
| `reputacion_mock.csv` | `metricas_reputacion` | 6 meses |
| `envios_mock.csv` | `metricas_envios` | 200 por cliente |
| `stock_mock.csv` | `metricas_stock` | 50 por cliente |

## Infraestructura Local
- **PostgreSQL 16**: `localhost:5432`
- **Metabase**: `http://localhost:3000`
- **Backend FastAPI**: `http://localhost:8000`
- La base maestra `dime_maestra` y las bases de cliente `dime_cliente_X` se crean via los scripts en `scripts/sql/init/` o via script de contingencia.
- Metabase usa su propia base `dime_metabase` en el mismo PostgreSQL.

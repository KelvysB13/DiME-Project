<div align="center">

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Segoe+UI&weight=600&size=30&duration=4000&pause=2000&color=FFFFFF&center=true&vCenter=true&width=1000&height=60&lines=%F0%9F%93%8A+DiME+-+Diagn%C3%B3stico+Integral+de+M%C3%A9tricas+E-Commerce" alt="Typing animation">
</p>

<p align="center">
  <img src="backend/assets/img/DiME_Banner.png" alt="DiME Banner" width="100%">
</p>

**Sistema de Diagnostico Automatizado para Vendedores de Mercado Libre**

<a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-0.136.3-green?logo=fastapi" alt="FastAPI 0.136.3">
</a>
<a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql" alt="PostgreSQL 16">
</a>
<a href="https://metabase.com/">
    <img src="https://img.shields.io/badge/Metabase-Latest-orange?logo=metabase" alt="Metabase">
</a>
<a href="#">
    <img src="https://img.shields.io/badge/Status-En%20Desarrollo-yellow" alt="Estado: En Desarrollo">
</a>

</div>

---

## Descripcion

**DiME** es un sistema SaaS que automatiza el diagnostico estrategico de vendedores en Mercado Libre. Extrae datos mediante API (OAuth 2.0) y los transforma en KPIs claros, reportes analiticos y planes de accion concretos.

### Areas de diagnostico

- **Comercial:** Maximiza ventas y posicionamiento.
- **Finanzas:** Evalua rentabilidad y salud economica.
- **Logistica:** Monitorea desempeno de envios y stock FULL.
- **Reputacion:** Controla reclamos, mediaciones e insignias.

---

## Instalacion y Uso

### Requisitos previos

| Herramienta | Version | Descarga |
|-------------|---------|----------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| PostgreSQL | 16 | [postgresql.org](https://www.postgresql.org/download/) |
| Java (JRE) | 17+ | [adoptium.net](https://adoptium.net/) |

### 1. Configurar PostgreSQL

1. Instala PostgreSQL 16 y crea el usuario y las bases de datos:

```bash
# Accede a psql como superusuario (el comando puede variar segun el SO)
psql -U postgres

CREATE USER dime_user WITH PASSWORD 'dime_pass_2026';
CREATE DATABASE dime_maestra WITH OWNER dime_user;
CREATE DATABASE dime_metabase WITH OWNER dime_user;
CREATE DATABASE dime_cliente_1 WITH OWNER dime_user;
CREATE DATABASE dime_cliente_2 WITH OWNER dime_user;
CREATE DATABASE dime_cliente_3 WITH OWNER dime_user;
\q
```

2. Ejecuta los scripts SQL de inicializacion en orden:

```bash
psql -U dime_user -d dime_maestra -f scripts/sql/init/02-schema-maestra.sql
psql -U dime_user -d dime_cliente_1 -f scripts/sql/init/03-schema-cliente.sql
```

### 2. Configurar Metabase

1. Descarga Metabase desde [metabase.com/start](https://www.metabase.com/start/) y ejecutalo:

```bash
java -jar metabase.jar
```

2. Abre http://localhost:3000, completa la configuracion inicial y conectalo a la base `dime_maestra` con credenciales `dime_user` / `dime_pass_2026`.

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con las credenciales de tu PostgreSQL local
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Iniciar el backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 6. Acceder a los servicios

| Servicio | URL |
|----------|-----|
| API FastAPI | http://localhost:8000 |
| Documentacion API | http://localhost:8000/docs |
| Metabase | http://localhost:3000 |
| Health Check | http://localhost:8000/health |

### 7. Cargar datos de contingencia (opcional)

```bash
python scripts/etl/cargar_datos_contingencia.py
```

### 8. Ejecutar tests

```bash
pytest tests -v
```

---

## Estructura del Proyecto

```text
DiME-Project/
|
+--- backend/                 # API - FastAPI
|   +--- app/
|   |   +--- main.py          # Punto de entrada
|   |   +--- config.py        # Configuracion (pydantic-settings)
|   |   +--- database.py      # Conexion PostgreSQL
|   |   |
|   |   +--- auth/            # Autenticacion OAuth 2.0
|   |       +--- routes.py    # Endpoints
|   |
|   +--- assets/              # Recursos visuales
|       +--- img/
|
+--- scripts/                 # Utilidades
|   +--- etl/                 # Scripts de carga de datos
|   |   +--- cargar_datos_contingencia.py
|   |   +--- conexion_api_ml.py
|   +--- sql/init/            # Inicializacion de base de datos
|       +--- 01-create-databases.sql
|       +--- 02-schema-maestra.sql
|       +--- 03-schema-cliente.sql
|
+--- data/                    # Datos de contingencia
|   +--- raw/                 # CSVs de entrada
|   +--- processed/           # Datos transformados
|
+--- docs/                    # Documentacion
|   +--- diagrama_er.md
|   +--- plan_contingencia.md
|
+--- tests/                   # Tests unitarios
|   +--- test_api.py
|   +--- test_database.py
|   +--- test_etl.py
|
+--- metabase/                # Exportacion de dashboards
|
+--- requirements.txt         # Dependencias del proyecto
+--- .env.example             # Template de variables de entorno
+--- .gitignore               # Archivos ignorados por git
+--- README.md
```

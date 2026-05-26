# 📊 DiME - Diagnóstico Integral de Métricas E-commerce

<p align="center">
  <img src="backend/assets/img/DiME_banner.svg" alt="DiME Banner" width="100%">
</p>

<div align="center">

<a href="https://www.python.org/downloads/release/python-3129/">
    <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python 3.12">
</a>
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

**Sistema de diagnóstico automatizado para vendedores de Mercado Libre**

</div>

---

## 📖 Descripción

**DiME** es un sistema SaaS que automatiza el diagnóstico estratégico de vendedores en Mercado Libre. Extrae datos mediante API (OAuth 2.0) y los transforma en KPIs claros, reportes analíticos y planes de acción concretos.

### Áreas de diagnóstico

- **Comercial:** Maximiza ventas y posicionamiento.
- **Finanzas:** Evalúa rentabilidad y salud económica.
- **Logística:** Monitorea desempeño de envíos y stock FULL.
- **Reputación:** Controla reclamos, mediaciones e insignias.

---

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
    ```text
    git clone https://github.com/tu-usuario/dime-project.git
    cd dime-project
    ```

2. **Crear entorno virtual e instalar dependencias:**
    ```text
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configurar variables de entorno:**
    ```text
    cp .env.example .env
    ```
    Editar `.env` con tus credenciales.

4. **Levantar infraestructura con Docker:**
    ```text
    cd scripts/docker
    docker compose up -d
    ```

5. **Iniciar el backend:**
    ```text
    cd backend
    uvicorn app.main:app --reload
    ```

6. **Cargar datos de contingencia (opcional):**
    ```text
    python scripts/etl/cargar_datos_contingencia.py
    ```

7. **Ejecutar tests:**
    ```text
    cd backend
    pytest ../tests
    ```

---

## 🗂️ Estructura del Proyecto

```text
DiME-Project/
│
├── 📁 backend/                  # API FastAPI
│   └── 📁 app/
│       ├── ⚙️ main.py          # Punto de entrada
│       ├── ⚙️ config.py        # Configuración (pydantic-settings)
│       ├── ⚙️ database.py      # Conexión PostgreSQL (psycopg2)
│       │
│       └── 📁 auth/            # Autenticación OAuth 2.0
│           └── ⚙️ routes.py    # Endpoints /auth/ml/*
│
├── 📁 scripts/                  # Utilidades
│   ├── 📁 etl/                 # Scripts de carga de datos
│   │   ├── ⚙️ cargar_datos_contingencia.py
│   │   └── ⚙️ conexion_api_ml.py
│   │
│   └── 📁 docker/              # Infraestructura
│       └── ⚙️ docker-compose.yml
│
├── 📁 data/                     # Datos de contingencia
│   ├── 📁 raw/                 # CSVs de entrada
│   └── 📁 processed/           # Datos transformados
│
├── 📁 docs/                     # Documentación
│   ├── 📄 diagrama_er.md
│   └── 📄 plan_contingencia.md
│
├── 📁 tests/                    # Tests unitarios
│   ├── ⚙️ test_api.py
│   ├── ⚙️ test_database.py
│   └── ⚙️ test_etl.py
│
├── 📁 metabase/                 # Exportación de dashboards
│
├── ⚙️ requirements.txt         # Dependencias del proyecto
├── ⚙️ .env.example             # Template de variables de entorno
├── ⚙️ .gitignore               # Archivos ignorados por git
└── 📄 README.md
```

---

## 🛠️ Tecnologías

| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.12 | Lenguaje principal |
| FastAPI | 0.136.3 | Backend mínimo (auth OAuth) |
| PostgreSQL | 16 | Base de datos multi-tenant |
| Metabase | Latest | Dashboards y visualización |
| psycopg2-binary | 2.9.10 | Conexión a PostgreSQL |
| pandas | 2.2.3 | Procesamiento ETL |
| PyJWT | 2.13.0 | Autenticación OAuth |
| Docker | Latest | Infraestructura local |
| pytest | 9.0.3 | Testing |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.

<div align="center">

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Segoe+UI&weight=600&size=30&duration=4000&pause=2000&color=FFFFFF&center=true&vCenter=true&width=1000&height=60&lines=%F0%9F%93%8A+DiME+-+Diagn%C3%B3stico+Integral+de+M%C3%A9tricas+E-Commerce" alt="Typing animation">
</p>

<p align="center">
  <img src="assets/images/DiME_Banner.png" alt="DiME Banner" width="100%">
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

## 📖 Descripcion

**DiME** es un sistema SaaS que automatiza el diagnostico estrategico de vendedores en Mercado Libre. Extrae datos mediante API (OAuth 2.0) y los transforma en KPIs claros, reportes analiticos y planes de accion concretos.

### 🎯 Areas de diagnostico

- **Comercial:** Maximiza ventas y posicionamiento.
- **Finanzas:** Evalua rentabilidad y salud economica.
- **Logistica:** Monitorea desempeno de envios y stock FULL.
- **Reputacion:** Controla reclamos, mediaciones e insignias.

---

## 🚀 Instalacion y Uso

### 📋 Requisitos previos

| Herramienta | Version | Descarga |
|-------------|---------|----------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| PostgreSQL | 16+ | [postgresql.org](https://www.postgresql.org/download/) |
| Java (JRE) | 17+ | [adoptium.net](https://adoptium.net/) |

### 🐘 1. Configurar PostgreSQL

1. Descarga PostgreSQL 16+ desde [postgresql.org](https://www.postgresql.org/download/).
2. Instala PostgreSQL siguiendo las indicaciones en su documentacion oficial.
3. Crear servidor personalizado.
4. Crear usuario administrador.
5. Crear base de datos.
6. Importar scripts SQL.

### 📊 2. Configurar Metabase

1. Descarga Metabase desde [metabase.com/start](https://www.metabase.com/start/) y ejecutalo:

```bash
java -jar metabase.jar
```

2. Abre http://localhost:3000, completa la configuracion inicial y conectalo a la base de datos maestra.

### 🔧 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con las credenciales de tu PostgreSQL local
```

### 📦 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### ▶️ 5. Iniciar el servidor

```bash
cd backend
uvicorn app.main:app --reload
```

### 🌐 6. Acceder a los servicios

| Servicio | URL |
|----------|-----|
| API FastAPI | http://localhost:8000 |
| Documentacion API | http://localhost:8000/docs |
| Metabase | http://localhost:3000 |
| Health Check | http://localhost:8000/health |

### 📥 7. Cargar datos de contingencia (opcional)

```bash
python scripts/etl/carga_datos.py
```

### ✅ 8. Ejecutar tests

```bash
pytest tests -v
```

---

## 📁 Estructura del Proyecto

```text
DiME-Project/
│
├── 🖥️ backend/                    # API - FastAPI
│   │
│   └── app/
│       │
│       ├── 🧠 core/               # Nucleo de la aplicacion
│       │   ├── config.py           
│       │   └── database.py 
│       │ 
│       ├── 🔐 auth/               # Autenticacion OAuth 2.0
│       │   └── auth_ml.py
│       │
│       ├── api_router.py           # Centralizador de rutas
│       └── main.py                 # Punto de entrada FastAPI
│
├── 📊 data/                        # Datos de contingencia
│   │
│   ├── raw/
│   └── processed/
│
├── 📚 docs/                        # Documentacion
│   │
│   └── plan_contingencia.md        # Plan de contingencia
│
├── 📈 metabase/                    # Exportacion de dashboards
│
├── 📜 scripts/                     # Utilidades
│   │
│   └── etl/
│       ├── carga_datos.py          # Carga de CSVs a PostgreSQL
│       └── conexion_ml.py          # ETL desde API de Mercado Libre
│
├── 🧪 tests/                      # Tests unitarios (pytest)
│   │
│   ├── pytest.ini                  # Configuracion de pytest
│   ├── test_api.py                 # Tests de endpoints
│   ├── test_database.py            # Tests de base de datos
│   └── test_etl.py                 # Tests de ETL/CSV
│
├── 📦 requirements.txt             # Dependencias del proyecto
├── 🔒 .env.example                 # Template de variables de entorno
├── 🙈 .gitignore                  # Archivos ignorados por git
│
└── 📖 README.md                   # Este archivo.
```

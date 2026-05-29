<div align="center">

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Segoe+UI&weight=600&size=30&duration=4000&pause=2000&color=FFFFFF&center=true&vCenter=true&width=1000&height=60&lines=%F0%9F%93%8A+DiME+-+Diagn%C3%B3stico+Integral+de+M%C3%A9tricas+E-Commerce" alt="Typing animation">
</p>

<p align="center">
  <img src="backend/assets/img/DiME_Banner.png" alt="DiME Banner" width="100%">
</p>

**Sistema de Diagnóstico Automatizado para Vendedores de Mercado Libre**

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

## 📖 Descripción

**DiME** es un sistema SaaS que automatiza el diagnóstico estratégico de vendedores en Mercado Libre. Extrae datos mediante API (OAuth 2.0) y los transforma en KPIs claros, reportes analíticos y planes de acción concretos.

### Áreas de diagnóstico

- **Comercial:** Maximiza ventas y posicionamiento.
- **Finanzas:** Evalúa rentabilidad y salud económica.
- **Logística:** Monitorea desempeño de envíos y stock FULL.
- **Reputación:** Controla reclamos, mediaciones e insignias.

---

## 🚀 Instalación y Uso

### Requisitos previos

| Herramienta | Versión | Descarga |
|-------------|---------|----------|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| Java (JRE) | 17+ | [adoptium.net](https://adoptium.net/) |
| Git | Última | [git-scm.com](https://git-scm.com/downloads) |

### 1. Clonar el repositorio

1. **Iniciar el backend:**
    ```text
    cd backend
    uvicorn app.main:app --reload
    ```

2. **Ejecutar tests:**
    ```text
    pytest tests -v
    ```

---

## 🗂️ Estructura del Proyecto

```text
DiME-Project/
│
├── 📁 backend/                 # API - FastAPI
│   ├── 📁 app/
│   │   ├── ⚙️ main.py          # Punto de entrada
│   │   ├── ⚙️ config.py        # Configuración (pydantic-settings)
│   │   ├── ⚙️ database.py      # Conexión PostgreSQL
│   │   │
│   │   └── 📁 auth/            # Autenticación OAuth 2.0
│   │       └── ⚙️ routes.py    # Endpoints
│   │
│   └── 📁 assets/              # Recursos visuales
│       └── 📁 images/          # Imagenes
│
├── 📁 scripts/                 # Utilidades
│   └── 📁 etl/                 # Scripts de carga de datos
│       │ 
│       ├── ⚙️ cargar_datos_contingencia.py
│       └── ⚙️ conexion_api_ml.py
│ 
│
├── 📁 data/                    # Datos de contingencia
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

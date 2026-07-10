# Auditoría DiME — Problemas detectados y correcciones

- **Total problemas listados:** 22 (P1 – P22)
- **Corregidos:** 15 (P1, P2, P3, P4, P6, P7, P10, P11, P12, P16, P17, P18, P19, P20, P21)
- **Saltados (no se tocaron):** 7 — P5, P8, P9, P13, P14, P15, P22

## ✅ P1 — CSS inline duplicado + lógica de controlador en vista
- **Archivo:** `views/public/user_settings.html`
- **Problema:** ~120 líneas de CSS inline que ya existían en `user_settings_style.css`; JS de UI mezclado en la vista.
- **Solución:** Reemplazado `<style>` inline por `<link>` a `user_settings_style.css`. JS ya estaba en `controllers/settingsController.js`, solo se dejó el `<script src="...">`.
- **Estado: CORREGIDO**

## ✅ P2 — URLs hardcodeadas a `http://127.0.0.1:8000/api`
- **Archivos afectados:** `loginController.js`, `paymentController.js`, `syncController.js`, `adminVendedoresController.js`, `authController.js`, `register.html`
- **Problema:** 6 archivos usaban `http://127.0.0.1:8000/api` en vez de `/api`.
- **Solución:** Reemplazado por `/api` en todos.
- **Estado: CORREGIDO**

## ✅ P3 — Endpoints admin sin autenticación
- **Archivos:** `backend/api/plan_router.py`, `backend/api/mockoon_router.py`
- **Problema:** POST/PUT/DELETE de planes y métricas mockoon no verificaban si el usuario era admin.
- **Solución:** Agregado `_verify_admin` vía `Depends(get_current_user)` + chequeo `isinstance(current_user, Admin)`.
- **Estado: CORREGIDO**

## ✅ P4 — Debug `print()` en producción
- **Archivos:** `backend/services/auth_service.py`, `backend/services/password_recovery_service.py`
- **Problema:** 3 `print()` con tokens y datos de query.
- **Solución:** Eliminados.
- **Estado: CORREGIDO**

## ⏭️ P5 — Funciones de servicio nunca llamadas
- **Problema:** 20 funciones de backend definidas en servicios pero nunca importadas ni llamadas desde ningún router.
- **Estado: NO SE TOCÓ**

## ✅ P6 — JS inline en register.html no migrado a controlador
- **Archivo:** `views/public/register.html` → `controllers/registerController.js`
- **Problema:** Cuatro bloques `<script>` inline (147 líneas) con lógica de registro, typewriter, detección de tarjeta, etc.
- **Solución:** Migrado todo a `registerController.js`. Solo quedaron las variables de Flask (`CSRF_TOKEN`, `TURNSTILE_SITEKEY`) en un inline mínimo. `detectCardBrand()` y `handleRegister()` expuestos globalmente para los `onclick`/`oninput` del HTML.
- **Estado: CORREGIDO**

## ✅ P7 — Funciones duplicadas admin_dashboard.html
- **Archivo:** `views/admin/admin_dashboard.html`
- **Problema:** `getPaisName()` definida tanto en `adminVendedoresController.js` como en el inline script.
- **Solución:** Eliminada la copia del inline script; la del controlador se usa en ambos contextos.
- **Estado: CORREGIDO**

## ⏭️ P8 — dashboardController.js sin usar
- **Problema:** `dashboardController.js` no se usa; `user_dashboard.html` tiene 200+ líneas de JS inline.
- **Estado: NO SE TOCÓ**

## ⏭️ P9 — Login forgot password link muerto
- **Problema:** El enlace "¿Olvidaste tu contraseña?" en el login no lleva a ninguna parte o está roto.
- **Estado: NO SE TOCÓ**

## ✅ P10 — `Integer` → `BigInteger` en modelos
- **Archivos:** 11 modelos (`publicacion_model.py`, `reporte_model.py`, `metrica_reputacion_model.py`, `metrica_negocio_model.py`, `metrica_costo_model.py`, `metrica_stock_model.py`, `metrica_pagina_model.py`, `rendimiento_model.py`, `metrica_calidad_model.py`, `plan_model.py`, `kpis_maestro_model.py`, `vendedor_model.py`).
- **Problema:** Columnas `Integer` podían desbordarse con altos volúmenes de datos.
- **Solución:** Migrado a `BigInteger`.
- **Estado: CORREGIDO**

## ✅ P11 — Endpoint mal escrito `/moockon-data`
- **Archivos:** `backend/api/mockoon_router.py`, `controllers/syncController.js`
- **Problema:** El endpoint se llamaba `/moockon-data` (typo).
- **Solución:** Corregido a `/mockoon-data` en backend y frontend.
- **Estado: CORREGIDO**

## ✅ P12 — Race condition en `MAX(id) + 1`
- **Archivo:** `backend/services/plan_service.py`
- **Problema:** `SELECT id ... ORDER BY id DESC` + 1 manual para nuevo ID, vulnerable a concurrencia.
- **Solución:** Cambiado a `SELECT COALESCE(MAX(id), 0) + 1` vía `func.max()`.
- **Estado: CORREGIDO**

## ⏭️ P13 — Dead Schema TokenRequest nunca importado
- **Problema:** El schema `TokenRequest` está definido pero nunca es importado ni usado en ningún endpoint.
- **Estado: NO SE TOCÓ**

## ⏭️ P14 — Dead Schema KpiMaestroCreate
- **Problema:** El schema `KpiMaestroCreate` está definido pero nunca se utiliza.
- **Estado: NO SE TOCÓ**

## ⏭️ P15 — Problema no especificado
- **Problema:** El usuario no recordaba el detalle. Era parte de los que no le preocupaban.
- **Estado: NO SE TOCÓ**

## ✅ P16 — CSS inline no referenciado
- **Archivo:** `views/public/user_settings.html`
- **Problema:** Mismo que P1; CSS inline duplicado.
- **Solución:** Reemplazado por `user_settings_style.css`.
- **Estado: CORREGIDO**

## ✅ P17 — Directorio vacío `assets/scripts/`
- **Solución:** Eliminado.
- **Estado: CORREGIDO**

## ✅ P18 — Comentarios de desarrollo (TODO/FIXME/DEBUG) en backend
- **Resultado:** No se encontraron en archivos `.py`.
- **Estado: CORREGIDO (no había nada que corregir)**

## ✅ P19 — FAQ sin ruta ni enlace en navegación
- **Archivo:** `views/public/home.html`
- **Problema:** La ruta `/faq` ya existía en `frontend_router.py` pero no había enlace en el header.
- **Solución:** Agregado `<a href="/faq">FAQ</a>` en la navegación de `home.html`.
- **Estado: CORREGIDO**

## ✅ P20 — `DROP TABLE IF EXISTS` en script SQL
- **Archivo:** `scripts/sql/dime_db.sql`
- **Problema:** 17 `DROP TABLE` + 1 `DROP EXTENSION` al inicio del script. Peligroso en producción.
- **Solución:** Eliminado todo el bloque DROP (líneas 10-43).
- **Estado: CORREGIDO**

## ✅ P21 — Separadores decorativos `-- ======` en dime_db.sql
- **Archivo:** `scripts/sql/dime_db.sql`
- **Problema:** 79 líneas de `-- ======` puramente decorativas.
- **Solución:** Eliminadas todas.
- **Estado: CORREGIDO**

## ⏭️ P22 — Responsive design pendiente
- **Problema:** El dashboard y otras vistas no están adaptadas para móviles/tablets. Faltaba agregar media queries y ajustar layouts. El usuario nunca lo empezó.
- **Estado: NO SE TOCÓ**

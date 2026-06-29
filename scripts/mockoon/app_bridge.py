from flask import Flask, request, jsonify
import psycopg2
# -*- coding: utf-8 -*-

app = Flask(__name__)

# Configuración de conexión segura a tu base de datos local
DB_CONFIG = {
    "dbname": "dime_DB",
    "user": "postgres",
    "password": "admin123",  # <-- Recuerda poner tu clave real de Postgres aquí
    "host": "localhost",
    "port": "5432"
}

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return response

@app.route('/api/guardar-metricas', methods=['POST', 'OPTIONS'])
def guardar_metricas():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    conn = None
    try:
        payload = request.json
        if not payload:
            return jsonify({"error": "Payload vacío"}), 400

        # Desempaquetamos los bloques según tu JSON real de Mockoon
        basicos = payload.get('datos_basicos', {})
        negocio = payload.get('metricas_negocio', {})
        costo = payload.get('metricas_costo', {})
        reputacion = payload.get('metricas_reputacion', {})
        stock_full = payload.get('metricas_stock_full', {})
        mi_pagina = payload.get('metricas_mi_pagina', {})

        print(f"📥 [BACKEND] Procesando e-commerce de: {basicos.get('nombre_tienda', 'Desconocido')}")

        plan_map = {
            "free": 1,
            "gratuito": 1,
            "plan gratuito": 1,
            "pro": 2,
            "plan pro": 2,
            "enterprise": 3,
            "premium": 3,
            "plan enterprise": 3
        }
        
        # Extraemos lo que mande Mockoon, lo pasamos a minúsculas y limpiamos espacios
        plan_recibido = str(basicos.get('tipo_plan', '1')).lower().strip()
        
        # Buscamos en el mapa. Si Mockoon manda algo raro, por defecto asignamos 1 (Plan Free)
        tipo_plan_id = plan_map.get(plan_recibido, 1)

        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8') 
        cursor = conn.cursor()

        # ==============================================================================
        # 1. TABLA: vendedor (Mapeo relacional con ON CONFLICT)
        # ==============================================================================
        query_vendedor = """
            INSERT INTO vendedor (user_name, nombre_tienda, codigo_pais, moneda_local, tipo_plan, email, esta_activo)
            VALUES (%s, %s, %s, %s, %s, %s, true)
            ON CONFLICT (user_name) 
            DO UPDATE SET 
                nombre_tienda = EXCLUDED.nombre_tienda, 
                tipo_plan = EXCLUDED.tipo_plan
            RETURNING id_vendedor;
        """
        cursor.execute(query_vendedor, (
            basicos.get('user_name'),
            basicos.get('nombre_tienda'),
            basicos.get('codigo_pais', 'MX'),
            basicos.get('moneda_local', 'MXN'),
            basicos.get('tipo_plan_id', 1),
            basicos.get('email', f"{basicos.get('user_name')}@test-dime.com")
        ))
        id_vendedor = cursor.fetchone()[0]

        # ==============================================================================
        # 2. TABLA: metricas_reputacion
        # ==============================================================================
        query_reputacion = """
            INSERT INTO metricas_reputacion (id_vendedor, ventas_totales_periodo, total_reclamos, total_mediaciones, total_canceladas, total_envios_incorrectos, nivel_reputacion, insignia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_vendedor) DO UPDATE SET
                total_reclamos = EXCLUDED.total_reclamos,
                nivel_reputacion = EXCLUDED.nivel_reputacion,
                insignia = EXCLUDED.insignia;
        """
        cursor.execute(query_reputacion, (
            id_vendedor,
            negocio.get('ventas_totales_periodo', 0),
            reputacion.get('total_reclamos', 0),
            reputacion.get('total_mediaciones', 0),
            reputacion.get('total_canceladas', 0),
            reputacion.get('total_envios_incorrectos', 0),
            reputacion.get('nivel_reputacion', 'green').lower(),
            reputacion.get('insignia', None)
        ))

        # ==============================================================================
        # 3. TABLA: metricas_negocio
        # ==============================================================================
        query_negocio = """
            INSERT INTO metricas_negocio (id_vendedor, fecha_inicio_periodo, fecha_fin_periodo, ventas_brutas_moneda_local, ventas_brutas_usd, unidades_vendidas, visitas_totales, intencion_compra, ventas_concretadas, precio_promedio_unidad, precio_promedio_venta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_vendedor) DO UPDATE SET
                ventas_brutas_moneda_local = EXCLUDED.ventas_brutas_moneda_local,
                visitas_totales = EXCLUDED.visitas_totales;
        """
        cursor.execute(query_negocio, (
            id_vendedor,
            negocio.get('fecha_inicio_periodo', '2026-05-01'),
            negocio.get('fecha_final_periodo', '2026-05-31'), # Mapeado exacto desde Mockoon
            negocio.get('ventas_brutas_moneda_local', 0.0),
            negocio.get('ventas_brutas_usd', 0.0),
            negocio.get('unidades_vendidas', 0),
            negocio.get('visitas_totales', 0),
            negocio.get('intencion_compra', 0),
            negocio.get('ventas_concretadas', 0),
            negocio.get('precio_promedio_unidad', 0.0),
            negocio.get('precio_promedio_venta', 0.0)
        ))

        # ==============================================================================
        # 4. TABLA: metricas_costo
        # ==============================================================================
        query_costo = """
            INSERT INTO metricas_costo (id_vendedor, ventas_cobradas_total, neto_recibido, cargos_por_venta, costos_envio, inversion_ads, otros_cargos, cargos_envio_full, descuento_reputacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_vendedor) DO UPDATE SET
                neto_recibido = EXCLUDED.neto_recibido;
        """
        cursor.execute(query_costo, (
            id_vendedor,
            costo.get('ventas_cobradas_total', 0.0),
            costo.get('neto_recibido', 0.0),
            costo.get('cargos_por_venta', 0.0),
            costo.get('costos_envio', 0.0),
            costo.get('inversion_ads', 0.0),
            costo.get('otros_cargos', 0.0),
            costo.get('cargos_envio_full', 0.0),
            costo.get('descuento_reputacion', 0.0)
        ))

        # ==============================================================================
        # 5. TABLA: metricas_stock_full
        # ==============================================================================
        query_stock = """
            INSERT INTO metricas_stock_full (id_vendedor, espacios_p_asignados, espacios_g_asignados, puntaje_calidad, productos_no_aptos_venta, productos_sin_rotacion, productos_antiguedad, productos_exceso_proyeccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_vendedor) DO UPDATE SET
                puntaje_calidad = EXCLUDED.puntaje_calidad;
        """
        cursor.execute(query_stock, (
            id_vendedor,
            stock_full.get('espacios_p_asignados', 0),
            stock_full.get('espacios_g_asignados', 0),
            stock_full.get('puntaje_calidad', 100),
            stock_full.get('productos_no_aptos_venta', 0),
            stock_full.get('productos_sin_rotacion', 0),
            stock_full.get('productos_antiguedad', 0),
            stock_full.get('productos_exceso_proyeccion', 0)
        ))

        # Guardar cambios
        conn.commit()
        cursor.close()
        print("✅ [POSTGRES] ¡Éxito total! Las métricas relacionales impactaron en tu DB.")
        return jsonify({"status": "success", "message": "Datos inyectados perfectamente en Postgres"}), 201

    except Exception as e:
        if conn:
            conn.rollback()
        print("\n🔥 [ALERTA DE BASE DE DATOS] Se detectó un error de SQL nativo.")
        print(f"-> Tipo de excepción: {type(e).__name__}")
        
        # Usamos repr() para evitar que el códec de Python falle con caracteres de Windows
        print(f"-> Representación segura (repr): {repr(e)}")
        
        # Si es un error propio de PostgreSQL, extraemos el código de estado (SQLSTATE)
        if hasattr(e, 'pgcode'):
            print(f"-> Código SQLSTATE de Postgres: {e.pgcode}")
            
        return jsonify({"error": "Error interno de base de datos descifrado en consola"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(port=8080, debug=True)
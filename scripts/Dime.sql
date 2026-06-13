-- ==============================================================================
-- DIME.sql - Base de datos para diagnóstico de métricas de vendedores
-- ==============================================================================
-- Este script crea el esquema de base de datos para una aplicación que
-- consume métricas de Mercado Libre (ventas, reputación, costos, stock, etc.)
-- y genera reportes de diagnóstico con plan de acción para cada vendedor.
-- ==============================================================================


-- ==============================================================================
-- TABLAS MAESTRAS (CATÁLOGOS DE REFERENCIA)
-- ==============================================================================
-- Estas tablas almacenan datos de referencia que se usan como catálogos
-- en toda la base de datos. No cambian frecuentemente.

-- TABLA: pais
-- Propósito: Catálogo de países donde operan los vendedores.
-- Cada país se identifica con su código ISO 3166-1 alpha-2 (2 letras).
CREATE TABLE IF NOT EXISTS pais (
    codigo_pais VARCHAR(2) PRIMARY KEY, -- Código ISO del país. Ej: 'AR' = Argentina, 'MX' = México
    nombre_pais VARCHAR(60) NOT NULL    -- Nombre completo del país. Ej: 'Argentina', 'México'
);

-- TABLA: moneda
-- Propósito: Catálogo de monedas utilizadas por los vendedores.
-- Cada moneda se identifica con su código ISO 4217 (3 letras).
CREATE TABLE IF NOT EXISTS moneda (
    codigo_moneda VARCHAR(3) PRIMARY KEY, -- Código ISO de la moneda. Ej: 'ARS', 'MXN', 'USD'
    nombre_moneda VARCHAR(50) NOT NULL,    -- Nombre descriptivo. Ej: 'Peso Argentino'
    simbolo VARCHAR(5) NOT NULL            -- Símbolo monetario. Ej: '$', 'R$', 'U$S'
);

-- TABLA: plan_saas
-- Propósito: Define los planes de suscripción del sistema SaaS.
-- El plan determina qué funcionalidades tiene disponible cada vendedor.
--   1 = Free:   plan gratuito con métricas básicas
--   2 = Pro:    plan pago con métricas avanzadas y reportes
--   3 = Enterprise: plan premium con soporte prioritario y multi-cuenta
CREATE TABLE IF NOT EXISTS plan_saas (
    id_plan INTEGER PRIMARY KEY, -- 1: Free, 2: Pro, 3: Enterprise
    nombre_plan VARCHAR(50) NOT NULL, -- Nombre comercial del plan
    descripcion TEXT                 -- Descripción detallada de beneficios
);


-- ==============================================================================
-- TABLA: vendedor
-- ==============================================================================
-- Propósito: Almacena los datos principales de cada vendedor registrado
-- en la plataforma. Es la tabla central del esquema; todas las demás
-- tablas de métricas apuntan a esta mediante foreign keys.
-- 
-- Cada vendedor pertenece a un país, opera con una moneda local,
-- tiene un plan de suscripción y almacena tokens de autenticación
-- para consumir la API de Mercado Libre.
CREATE TABLE IF NOT EXISTS vendedor (
    -- Identidad del vendedor
    id_vendedor BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado, único para cada vendedor
    user_name VARCHAR(50) NOT NULL UNIQUE,       -- Nombre de usuario único en la plataforma
    nombre_tienda VARCHAR(100) NOT NULL,          -- Nombre comercial de la tienda
    
    -- Relaciones con tablas maestras
    codigo_pais VARCHAR(2) NOT NULL,  -- País donde opera el vendedor (FK -> pais)
    moneda_local VARCHAR(3) NOT NULL,  -- Moneda en la que factura (FK -> moneda)
    tipo_plan INTEGER DEFAULT 1,       -- Plan SaaS contratado, 1=Free por defecto (FK -> plan_saas)
    
    -- Datos de autenticación y conexión con Mercado Libre
    email VARCHAR(255) NOT NULL UNIQUE, -- Correo electrónico del vendedor (único en el sistema)
    access_token TEXT,                  -- Token de acceso a la API de ML (se renueva periódicamente)
    refresh_token TEXT,                 -- Token para renovar el access_token sin pedir credenciales
    tiempo_token TIMESTAMPTZ,           -- Fecha/hora de expiración/emisión del token
    esta_activo BOOLEAN NOT NULL DEFAULT TRUE, -- Indica si la cuenta está activa (false = deshabilitada)
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Fecha de registro del vendedor
    
    -- Restricciones de Integridad Referencial (Foreign Keys)
    CONSTRAINT fk_vendedor_pais FOREIGN KEY (codigo_pais) REFERENCES pais(codigo_pais),
    CONSTRAINT fk_vendedor_moneda FOREIGN KEY (moneda_local) REFERENCES moneda(codigo_moneda),
    CONSTRAINT fk_vendedor_plan FOREIGN KEY (tipo_plan) REFERENCES plan_saas(id_plan),
    
    -- Validación de formato de email mediante expresión regular
    -- Asegura que el email tenga el formato: usuario@dominio.ext (ext de 2 a 4 letras)
    CONSTRAINT chk_email_formato CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
);


-- ==============================================================================
-- TABLA: publicacion
-- ==============================================================================
-- Propósito: Almacena las publicaciones (anuncios) que cada vendedor tiene
-- activas en Mercado Libre. Una publicación es un producto listado para
-- la venta en la plataforma.
-- 
-- Cada publicación pertenece a un único vendedor y tiene un identificador
-- único de ML (ml_item_id) con prefijo que indica el país (MLA=Argentina,
-- MLB=Brasil, MLC=Chile, MLM=México, MLV=Venezuela, etc.).
CREATE TABLE IF NOT EXISTS publicacion (
    id_publicacion BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la publicación
    id_vendedor BIGINT NOT NULL,          -- Vendedor propietario de la publicación (FK -> vendedor)
    ml_item_id VARCHAR(20) NOT NULL UNIQUE, -- ID único que ML asigna a la publicación. Ej: 'MLA123456789'
    titulo VARCHAR(100) NOT NULL,         -- Título de la publicación (ML lo limita a 60 caracteres aprox.)
    tipo_publicacion VARCHAR(20) NOT NULL CHECK (tipo_publicacion IN ('classic', 'gold_pro', 'premium')), -- Tipo de listado: classic (gratuito), gold_pro (destacado), premium (premium)
    estado_publicacion VARCHAR(20) NOT NULL CHECK (estado_publicacion IN ('active', 'paused', 'closed')), -- Estado: active (activa), paused (pausada), closed (cerrada)
    
    CONSTRAINT fk_publicacion_vendedor FOREIGN KEY (id_vendedor) 
        REFERENCES vendedor(id_vendedor) ON DELETE CASCADE -- Si se elimina el vendedor, se eliminan sus publicaciones
);


-- ==============================================================================
-- TABLA: reportes_diagnostico
-- ==============================================================================
-- Propósito: Almacena los reportes generados automáticamente para cada
-- vendedor. Cada reporte contiene un resumen ejecutivo del desempeño
-- del vendedor en un período y un plan de acción en formato JSON con
-- recomendaciones personalizadas para mejorar sus métricas.
-- 
-- El plan_accion es JSONB (binario) lo que permite consultas flexibles
-- sobre las tareas recomendadas sin esquema fijo.
CREATE TABLE IF NOT EXISTS reportes_diagnostico (
    id_reporte BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado del reporte
    id_vendedor BIGINT NOT NULL,                    -- Vendedor al que pertenece el reporte (FK -> vendedor)
    fecha_generacion DATE NOT NULL DEFAULT CURRENT_DATE, -- Fecha en que se generó el reporte
    fecha_inicio_periodo DATE NOT NULL,              -- Inicio del período analizado
    fecha_fin_periodo DATE NOT NULL,                 -- Fin del período analizado
    resumen_ejecutivo TEXT,                          -- Texto libre con análisis general del desempeño
    plan_accion JSONB NOT NULL DEFAULT '{}'::jsonb,  -- Lista de tareas recomendadas en formato JSON
    
    CONSTRAINT fk_reportes_vendedor FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor),
    CONSTRAINT chk_fechas_reporte CHECK (fecha_fin_periodo >= fecha_inicio_periodo) -- La fecha fin no puede ser anterior a la fecha inicio
);


-- ==============================================================================
-- TABLA: metricas_reputacion
-- ==============================================================================
-- Propósito: Almacena las métricas de reputación de cada vendedor.
-- La reputación en Mercado Libre se calcula en base a reclamos,
-- mediaciones, cancelaciones y envíos incorrectos.
-- 
-- El nivel de reputación puede ser:
--   'green'  = buena reputación
--   'yellow' = reputación en riesgo
--   'red'    = mala reputación
-- La insignia es un reconocimiento especial: 'platinum', 'gold', 'leader', etc.
CREATE TABLE IF NOT EXISTS metricas_reputacion (
  id_metricas_reputacion BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la métrica de reputación
  id_vendedor BIGINT NOT NULL UNIQUE, -- Vendedor evaluado (FK -> vendedor, 1:1)
  fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura de la métrica
  ventas_totales_periodo INTEGER NOT NULL DEFAULT 0 CHECK (ventas_totales_periodo >= 0), -- Ventas totales en el período
  total_reclamos INTEGER NOT NULL DEFAULT 0 CHECK (total_reclamos >= 0), -- Reclamos recibidos por el vendedor
  total_mediaciones INTEGER NOT NULL DEFAULT 0 CHECK (total_mediaciones >= 0), -- Mediaciones abiertas por compradores
  total_canceladas INTEGER NOT NULL DEFAULT 0 CHECK (total_canceladas >= 0), -- Ventas canceladas por ML
  total_envios_incorrectos INTEGER NOT NULL DEFAULT 0 CHECK (total_envios_incorrectos >= 0), -- Envíos entregados incorrectamente
  nivel_reputacion VARCHAR(20) NOT NULL, -- Nivel: 'green', 'yellow', 'red'
  insignia VARCHAR(20), -- Insignia: 'platinum', 'gold', 'leader' o NULL
  FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor)
);


-- ==============================================================================
-- TABLA: metricas_negocio
-- ==============================================================================
-- Propósito: Almacena las métricas comerciales clave de cada vendedor.
-- Contiene información sobre ventas (en moneda local y USD), visitas,
-- intención de compra y precios promedio.
-- 
-- Los precios promedio se calculan a partir de los totales:
--   precio_promedio_unidad = ventas_brutas / unidades_vendidas
--   precio_promedio_venta  = ventas_brutas / ventas_concretadas
CREATE TABLE IF NOT EXISTS metricas_negocio (
  id_metricas_negocio BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la métrica de negocio
  id_vendedor BIGINT NOT NULL UNIQUE, -- Vendedor evaluado (FK -> vendedor, 1:1)
  fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura de la métrica
  fecha_inicio_periodo DATE NOT NULL, -- Inicio del período analizado
  fecha_fin_periodo DATE NOT NULL, -- Fin del período analizado
  ventas_brutas_moneda_local NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (ventas_brutas_moneda_local >= 0), -- Ventas brutas en moneda local
  ventas_brutas_usd NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (ventas_brutas_usd >= 0), -- Ventas brutas convertidas a USD
  unidades_vendidas INTEGER NOT NULL DEFAULT 0 CHECK (unidades_vendidas >= 0), -- Cantidad de unidades vendidas
  visitas_totales INTEGER NOT NULL DEFAULT 0 CHECK (visitas_totales >= 0), -- Visitas totales a las publicaciones
  intencion_compra INTEGER NOT NULL DEFAULT 0 CHECK (intencion_compra >= 0), -- Usuarios que hicieron clic en "Comprar"
  ventas_concretadas INTEGER NOT NULL DEFAULT 0 CHECK (ventas_concretadas >= 0), -- Ventas efectivamente concretadas
  precio_promedio_unidad NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (precio_promedio_unidad >= 0), -- Precio promedio por unidad (ventas_brutas / unidades_vendidas)
  precio_promedio_venta NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (precio_promedio_venta >= 0), -- Precio promedio por venta (ventas_brutas / ventas_concretadas)
  FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor)
);


-- ==============================================================================
-- TABLA: metricas_costo
-- ==============================================================================
-- Propósito: Almacena el desglose de costos y comisiones que ML cobra
-- a cada vendedor. Permite calcular el neto recibido después de todos
-- los descuentos y entender dónde se están yendo los márgenes.
-- 
-- Estructura de costos típica:
--   neto_recibido = ventas_cobradas_total - cargos_por_venta - costos_envio
--                   - inversion_ads - otros_cargos - cargos_envio_full
--                   - descuento_reputacion
CREATE TABLE IF NOT EXISTS metricas_costo (
  id_metricas_costo BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la métrica de costo
  id_vendedor BIGINT NOT NULL UNIQUE, -- Vendedor evaluado (FK -> vendedor, 1:1)
  fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura de la métrica
  ventas_cobradas_total NUMERIC(15,2) NOT NULL DEFAULT 0.00, -- Total de ventas cobradas por ML
  neto_recibido NUMERIC(15,2) NOT NULL DEFAULT 0.00, -- Neto recibido después de todos los descuentos
  cargos_por_venta NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (cargos_por_venta >= 0), -- Comisión de ML por venta
  costos_envio NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (costos_envio >= 0), -- Costos de envío (0 si usa Full)
  inversion_ads NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (inversion_ads >= 0), -- Inversión en publicidad (Mercado Ads)
  otros_cargos NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (otros_cargos >= 0), -- Otros cargos adicionales de ML
  cargos_envio_full NUMERIC(15,2) NOT NULL DEFAULT 0.00 CHECK (cargos_envio_full >= 0), -- Cargos de logística Full
  descuento_reputacion NUMERIC(15,2) NOT NULL DEFAULT 0.00, -- Penalización por reputación baja (yellow/red)
  FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor)
);


-- ==============================================================================
-- TABLA: metricas_stock_full
-- ==============================================================================
-- Propósito: Almacena métricas del programa Full de Mercado Libre
-- (logística administrada por ML). Los vendedores que participan en
-- Full envían su stock a centros de distribución de ML.
-- 
-- Métricas clave:
--   - espacios asignados: cantidad de espacios en centros de distribución
--   - puntaje_calidad: calidad del stock en escala 0-100
--   - productos problemáticos: no aptos, sin rotación, con antigüedad, etc.
CREATE TABLE IF NOT EXISTS metricas_stock_full (
  id_metricas_stock BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la métrica de stock Full
  id_vendedor BIGINT NOT NULL UNIQUE, -- Vendedor evaluado (FK -> vendedor, 1:1)
  fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura de la métrica
  espacios_p_asignados INTEGER NOT NULL DEFAULT 0 CHECK (espacios_p_asignados >= 0), -- Espacios pequeños asignados en CD de ML
  espacios_g_asignados INTEGER NOT NULL DEFAULT 0 CHECK (espacios_g_asignados >= 0), -- Espacios grandes asignados en CD de ML
  puntaje_calidad INTEGER NOT NULL CHECK (puntaje_calidad BETWEEN 0 AND 100), -- Calidad del inventario (0-100)
  productos_no_aptos_venta INTEGER NOT NULL DEFAULT 0 CHECK (productos_no_aptos_venta >= 0), -- Productos dañados o no aptos para venta
  productos_sin_rotacion INTEGER NOT NULL DEFAULT 0 CHECK (productos_sin_rotacion >= 0), -- Productos sin rotación (baja demanda)
  productos_antiguedad INTEGER NOT NULL DEFAULT 0 CHECK (productos_antiguedad >= 0), -- Productos con antigüedad excesiva en CD
  productos_exceso_proyeccion INTEGER NOT NULL DEFAULT 0 CHECK (productos_exceso_proyeccion >= 0), -- Productos en exceso vs proyección de ventas
  FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor)
);


-- ==============================================================================
-- TABLA: metricas_mi_pagina
-- ==============================================================================
-- Propósito: Almacena métricas sobre la personalización de la página
-- oficial del vendedor en Mercado Libre ("Mi Página").
-- 
-- Una página bien configurada (con banner, logo, carruseles y categorías
-- organizadas) generalmente tiene mejor tasa de conversión porque
-- genera más confianza en el comprador.
CREATE TABLE IF NOT EXISTS metricas_mi_pagina (
  id_metricas_pagina BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la métrica de Mi Página
  id_vendedor BIGINT NOT NULL UNIQUE, -- Vendedor evaluado (FK -> vendedor, 1:1)
  fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura de la métrica
  tiene_banner BOOLEAN NOT NULL DEFAULT FALSE, -- Indica si la página tiene banner personalizado
  tiene_logo BOOLEAN NOT NULL DEFAULT FALSE, -- Indica si la página tiene logo personalizado
  tiene_carruseles BOOLEAN NOT NULL DEFAULT FALSE, -- Indica si tiene carruseles de productos
  categorias_organizadas BOOLEAN NOT NULL DEFAULT FALSE, -- Indica si las categorías están organizadas
  FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor)
);


-- ==============================================================================
-- TABLA: rendimiento_publicacion
-- ==============================================================================
-- Propósito: Almacena el rendimiento individual de cada publicación.
-- Permite analizar qué publicaciones específicas están funcionando bien
-- y cuáles necesitan optimización.
-- 
-- La relación visitas/ventas da la tasa de conversión de cada publicación.
-- Por ejemplo, si una publicación tiene 1000 visitas y 50 ventas,
-- su conversión es del 5%.
CREATE TABLE IF NOT EXISTS rendimiento_publicacion (
    id_rendimiento_publi BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado
    id_publicacion BIGINT NOT NULL,           -- Publicación evaluada (FK -> publicacion)
    fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura
    fecha_inicio_periodo DATE NOT NULL,        -- Inicio del período analizado
    fecha_fin_periodo DATE NOT NULL,           -- Fin del período analizado
    visitas INTEGER NOT NULL DEFAULT 0 CHECK (visitas >= 0), -- Cantidad de visitas que recibió la publicación
    ventas INTEGER NOT NULL DEFAULT 0 CHECK (ventas >= 0), -- Ventas generadas por esta publicación
    
    CONSTRAINT fk_rendimiento_publicacion FOREIGN KEY (id_publicacion) 
        REFERENCES publicacion(id_publicacion) ON DELETE CASCADE, -- Si se elimina la publicación, se elimina su rendimiento
    CONSTRAINT chk_fechas_rendimiento CHECK (fecha_fin_periodo >= fecha_inicio_periodo)
);


-- ==============================================================================
-- TABLA: metricas_calidad_publicacion
-- ==============================================================================
-- Propósito: Almacena métricas de calidad de cada publicación.
-- ML asigna un puntaje de calidad (0-100) basado en la cantidad de
-- fotos, si tiene video, si las características están completas, etc.
-- 
-- Las publicaciones con mayor puntaje de calidad suelen tener mejor
-- posicionamiento en los resultados de búsqueda de ML.
CREATE TABLE IF NOT EXISTS metricas_calidad_publicacion (
  id_metricas_calidad_publi BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- ID auto-generado de la métrica de calidad
  id_publicacion BIGINT NOT NULL UNIQUE, -- Publicación evaluada (FK -> publicacion, 1:1)
  fecha_captura TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Momento de captura de la métrica
  cantidad_fotos INTEGER NOT NULL DEFAULT 0 CHECK (cantidad_fotos >= 0), -- Cantidad de fotos de la publicación
  tiene_video BOOLEAN NOT NULL DEFAULT FALSE, -- Indica si la publicación tiene video
  caracteristicas_completas BOOLEAN NOT NULL DEFAULT FALSE, -- Indica si todas las características están completas
  puntaje_calidad INTEGER NOT NULL CHECK (puntaje_calidad BETWEEN 0 AND 100), -- Puntaje de calidad de ML (0-100)
  FOREIGN KEY (id_publicacion) REFERENCES publicacion(id_publicacion)
);

-- ==============================================================================
-- INSERCIÓN DE DATOS MAESTROS INICIALES
-- ==============================================================================
-- Estos inserts cargan los catálogos de referencia necesarios para
-- que la base de datos funcione correctamente.
-- Usan ON CONFLICT DO NOTHING para poder ejecutar el script múltiples
-- veces sin duplicar datos.

-- Inserts de Países
-- Se cargan 6 países de Latinoamérica donde opera Mercado Libre.
-- Cada país tiene su propia moneda y mercado (MLA, MLB, MLC, MLM, MLV).
INSERT INTO pais (codigo_pais, nombre_pais) VALUES 
('AR', 'Argentina'), 
('MX', 'México'), 
('BR', 'Brasil'), 
('CO', 'Colombia'), 
('CL', 'Chile'), 
('VE', 'Venezuela')
ON CONFLICT (codigo_pais) DO NOTHING;

-- Inserts de Monedas con sus símbolos
-- Cada país usa su moneda local. Venezuela (VE) usa USD porque su
-- moneda local (VES/Bs) no es estable ni práctica para comercio digital.
INSERT INTO moneda (codigo_moneda, nombre_moneda, simbolo) VALUES 
('ARS', 'Peso Argentino', '$'), 
('MXN', 'Peso Mexicano', '$'), 
('BRL', 'Real Brasileño', 'R$'), 
('COP', 'Peso Colombiano', '$'), 
('CLP', 'Peso Chileno', '$'), 
('USD', 'Dólar Estadounidense', '$')
ON CONFLICT (codigo_moneda) DO NOTHING;

-- Inserts de Planes SaaS
-- Se definen 3 planes con diferentes niveles de funcionalidad.
INSERT INTO plan_saas (id_plan, nombre_plan, descripcion) VALUES 
(1, 'Plan Gratuito', 'Prueba gratis por 7 días con acceso básico a métricas.'),
(2, 'Plan Pro', 'Métricas avanzadas, reportes y descargas ilimitadas.'),
(3, 'Plan Enterprise', 'Soporte prioritario, reportes a medida y multi-cuenta.')
ON CONFLICT (id_plan) DO NOTHING;


-- ==============================================================================
-- INSERCIÓN DE DATOS DE PRUEBA: VENDEDORES
-- ==============================================================================
-- Se insertan 18 vendedores de prueba distribuidos en 6 países (3 por país).
-- Cada vendedor tiene un plan distinto para poder probar todos los escenarios.
-- El vendedor 6 (ferreteria_mx) está inactivo para probar ese caso de uso.
-- Venezuela usa USD porque su moneda local no es práctica para e-commerce.
-- Los tokens son ficticios para pruebas.
INSERT INTO vendedor (
    user_name, 
    nombre_tienda, 
    codigo_pais, 
    moneda_local, 
    tipo_plan, 
    email, 
    access_token, 
    refresh_token, 
    tiempo_token, 
    esta_activo
) VALUES 
-- Vendedores de Argentina (AR / ARS)
-- 3 vendedores: uno Enterprise (tech), uno Pro (deco), uno Free (gaming)
('tech_guru_ar', 'Tech Guru Argentina', 'AR', 'ARS', 3, 'contacto@techguru.com.ar', 'acc_tk_01', 'ref_tk_01', CURRENT_TIMESTAMP, true),
('home_deco_ar', 'Home & Deco Baires', 'AR', 'ARS', 2, 'hola@homedecoar.com', 'acc_tk_02', 'ref_tk_02', CURRENT_TIMESTAMP, true),
('gaming_ar', 'Gaming Store AR', 'AR', 'ARS', 1, 'soporte@gamingar.com.ar', 'acc_tk_03', 'ref_tk_03', CURRENT_TIMESTAMP, true),

-- Vendedores de México (MX / MXN)
-- El vendedor 6 (ferreteria) está inactivo para probar el comportamiento del sistema con cuentas deshabilitadas
('moda_mx_oficial', 'Moda MX Oficial', 'MX', 'MXN', 2, 'ventas@modamx.com.mx', 'acc_tk_04', 'ref_tk_04', CURRENT_TIMESTAMP, true),
('autos_repuestos_mx', 'Repuestos Automotrices MX', 'MX', 'MXN', 3, 'contacto@repuestosmx.com', 'acc_tk_05', 'ref_tk_05', CURRENT_TIMESTAMP, true),
('ferreteria_mx', 'La Gran Ferretería', 'MX', 'MXN', 2, 'ventas@ferreteriamx.com', 'acc_tk_06', 'ref_tk_06', CURRENT_TIMESTAMP, false), -- Vendedor inactivo (prueba)

-- Vendedores de Brasil (BR / BRL)
('brasil_sports', 'Brasil Sports SA', 'BR', 'BRL', 1, 'contato@brasilsports.com.br', 'acc_tk_07', 'ref_tk_07', CURRENT_TIMESTAMP, true),
('beleza_br', 'Beleza Store Brasil', 'BR', 'BRL', 2, 'sac@belezabr.com', 'acc_tk_08', 'ref_tk_08', CURRENT_TIMESTAMP, true),
('calcados_br', 'Sapatos e Cia', 'BR', 'BRL', 3, 'atendimento@calcados.br', 'acc_tk_09', 'ref_tk_09', CURRENT_TIMESTAMP, true),

-- Vendedores de Colombia (CO / COP)
('colombia_coffee', 'Café de Colombia Shop', 'CO', 'COP', 2, 'info@cafecolombia.co', 'acc_tk_10', 'ref_tk_10', CURRENT_TIMESTAMP, true),
('juguetes_co', 'Juguetería Bogotá', 'CO', 'COP', 1, 'pedidos@juguetesco.com', 'acc_tk_11', 'ref_tk_11', CURRENT_TIMESTAMP, true),
('mascotas_co', 'Mascotas Felices CO', 'CO', 'COP', 1, 'hola@mascotasco.com', 'acc_tk_12', 'ref_tk_12', CURRENT_TIMESTAMP, true),

-- Vendedores de Chile (CL / CLP)
('chile_wines', 'Vinos Chilenos Premium', 'CL', 'CLP', 3, 'ventas@chilewines.cl', 'acc_tk_13', 'ref_tk_13', CURRENT_TIMESTAMP, true),
('libros_cl', 'Librería Santiago', 'CL', 'CLP', 2, 'contacto@libroscl.com', 'acc_tk_14', 'ref_tk_14', CURRENT_TIMESTAMP, true),
('deportes_cl', 'Deportes Extremos CL', 'CL', 'CLP', 2, 'ventas@deportescl.com', 'acc_tk_15', 'ref_tk_15', CURRENT_TIMESTAMP, true),

-- Vendedores de Venezuela (VE / USD)
-- Venezuela usa USD porque el Bolívar (VES) no es práctico para transacciones digitales
('ve_electronics', 'Venezuela Electronics', 'VE', 'USD', 1, 'sales@ve-electronics.com', 'acc_tk_16', 'ref_tk_16', CURRENT_TIMESTAMP, true),
('ropa_ve', 'Boutique Caracas', 'VE', 'USD', 1, 'info@ropave.com', 'acc_tk_17', 'ref_tk_17', CURRENT_TIMESTAMP, true),
('tecnologia_global_ve', 'Tecno Global VE', 'VE', 'USD', 3, 'admin@tecnoglobal.ve', 'acc_tk_18', 'ref_tk_18', CURRENT_TIMESTAMP, true);


-- ==============================================================================
-- 1. INSERCIÓN DE PUBLICACIONES (25 publicaciones)
-- ==============================================================================
-- Se insertan 25 publicaciones distribuidas entre los 18 vendedores.
-- Algunos vendedores tienen 1 publicación y otros tienen 2 o 3, según
-- su nivel de actividad.
-- 
-- Los ml_item_id tienen prefijos según el país:
--   MLA = Argentina, MLM = México, MLB = Brasil
--   MLC = Colombia/Chile, MLV = Venezuela
-- Los estados varían entre 'active', 'paused' y 'closed' para probar
-- los diferentes filtros del sistema.
INSERT INTO publicacion (id_vendedor, ml_item_id, titulo, tipo_publicacion, estado_publicacion) VALUES 
(1, 'MLA11111111', 'Auriculares Inalámbricos Bluetooth', 'premium', 'active'),
(1, 'MLA11111112', 'Teclado Mecánico Gamer RGB', 'classic', 'active'),
(2, 'MLA22222221', 'Lámpara de Escritorio LED', 'premium', 'active'),
(3, 'MLA33333331', 'Silla Gamer Ergonómica', 'gold_pro', 'active'),
(4, 'MLM44444441', 'Zapatos de Vestir Hombre', 'classic', 'paused'),
(4, 'MLM44444442', 'Tenis Deportivos Mujer', 'premium', 'active'),
(5, 'MLM55555551', 'Amortiguadores Delanteros Auto', 'gold_pro', 'active'),
(6, 'MLM66666661', 'Taladro Percutor Inalámbrico', 'classic', 'active'),
(7, 'MLB77777771', 'Bola de Futebol Oficial', 'premium', 'active'),
(8, 'MLB88888881', 'Kit Maquiagem Profissional', 'classic', 'active'),
(8, 'MLB88888882', 'Secador de Cabelo Íons', 'premium', 'paused'),
(9, 'MLB99999991', 'Tênis de Corrida', 'gold_pro', 'active'),
(10, 'MLC10101010', 'Café Tostado en Grano 1kg', 'premium', 'active'),
(11, 'MLC11111111', 'Figura de Acción Coleccionable', 'classic', 'active'),
(11, 'MLC11111112', 'Juego de Mesa Estrategia', 'premium', 'active'),
(12, 'MLC12121212', 'Cama para Perro Raza Grande', 'classic', 'active'),
(13, 'MLC13131313', 'Vino Tinto Reserva 750ml', 'gold_pro', 'active'),
(14, 'MLC14141414', 'Libro: Hábitos Atómicos', 'premium', 'active'),
(15, 'MLC15151515', 'Bicicleta de Montaña Aro 29', 'gold_pro', 'paused'),
(16, 'MLV16161616', 'Smart TV 55 Pulgadas 4K', 'premium', 'active'),
(16, 'MLV16161617', 'Smartphone Gama Media 128GB', 'classic', 'active'),
(17, 'MLV17171717', 'Chaqueta de Cuero Sintético', 'classic', 'active'),
(18, 'MLV18181818', 'Laptop Core i7 16GB RAM', 'gold_pro', 'active'),
(18, 'MLV18181819', 'Monitor Curvo 27 Pulgadas', 'premium', 'active'),
(18, 'MLV18181820', 'Mouse Inalámbrico Silencioso', 'classic', 'paused');


-- ==============================================================================
-- 2. INSERCIÓN DE REPORTES DE DIAGNÓSTICO (18 reportes)
-- ==============================================================================
-- Un reporte por cada vendedor. Cada reporte contiene:
--   - resumen_ejecutivo: análisis en texto libre del desempeño mensual
--   - plan_accion: tareas recomendadas en formato JSON para mejorar métricas
-- 
-- Los planes de acción varían según la situación de cada vendedor:
--   - Vendedores con buen desempeño: tareas de mantenimiento/expansión
--   - Vendedores con problemas: tareas correctivas (embalaje, calidad, etc.)
--   - Vendedores inactivos: tareas de reactivación
INSERT INTO reportes_diagnostico (id_vendedor, fecha_inicio_periodo, fecha_fin_periodo, resumen_ejecutivo, plan_accion) VALUES 
(1, '2023-10-01', '2023-10-31', 'Buen desempeño mensual, oportunidad en retención.', '{"tarea1": "Mejorar fotos", "tarea2": "Ajustar precios"}'),
(2, '2023-10-01', '2023-10-31', 'Ventas estables, revisar stock de productos clave.', '{"tarea1": "Reabastecer inventario"}'),
(3, '2023-10-01', '2023-10-31', 'Caída leve en conversión.', '{"tarea1": "Activar Ads", "tarea2": "Revisar competencia"}'),
(4, '2023-10-01', '2023-10-31', 'Excelente mes, mantener estrategia actual.', '{}'),
(5, '2023-10-01', '2023-10-31', 'Alto índice de reclamos.', '{"tarea1": "Mejorar embalaje", "tarea2": "Validar calidad"}'),
(6, '2023-10-01', '2023-10-31', 'Cuenta inactiva la mayor parte del mes.', '{"tarea1": "Reactivar publicaciones"}'),
(7, '2023-10-01', '2023-10-31', 'Crecimiento sostenido en envíos Full.', '{"tarea1": "Enviar más stock a bodega"}'),
(8, '2023-10-01', '2023-10-31', 'Ventas impulsadas por estacionalidad.', '{}'),
(9, '2023-10-01', '2023-10-31', 'Márgenes ajustados por altos costos de envío.', '{"tarea1": "Optimizar dimensiones de paquetes"}'),
(10, '2023-10-01', '2023-10-31', 'Fidelización alta, clientes recurrentes.', '{"tarea1": "Crear cupones de descuento"}'),
(11, '2023-10-01', '2023-10-31', 'Baja visibilidad en orgánico.', '{"tarea1": "Mejorar títulos", "tarea2": "Completar ficha técnica"}'),
(12, '2023-10-01', '2023-10-31', 'Métricas dentro de lo normal.', '{}'),
(13, '2023-10-01', '2023-10-31', 'Líder en su categoría este mes.', '{"tarea1": "Mantener calidad", "tarea2": "Expandir catálogo"}'),
(14, '2023-10-01', '2023-10-31', 'Ticket promedio bajo.', '{"tarea1": "Armar kits de productos"}'),
(15, '2023-10-01', '2023-10-31', 'Problemas con tiempos de despacho.', '{"tarea1": "Contratar logística externa"}'),
(16, '2023-10-01', '2023-10-31', 'Altas devoluciones por fallas técnicas.', '{"tarea1": "Cambiar proveedor"}'),
(17, '2023-10-01', '2023-10-31', 'Pocas ventas, falta de stock de tallas.', '{"tarea1": "Actualizar variantes"}'),
(18, '2023-10-01', '2023-10-31', 'Ventas récord por campaña promocional.', '{"tarea1": "Preparar stock para el próximo mes"}');


-- ==============================================================================
-- 3. INSERCIÓN DE MÉTRICAS DE REPUTACIÓN (18 registros)
-- ==============================================================================
-- Cada vendedor tiene un nivel de reputación que depende de sus reclamos,
-- mediaciones, cancelaciones y envíos incorrectos.
-- 
-- Escenarios representados:
--   - green/platinum: excelente reputación (v1, v7, v13, v18)
--   - green/gold: buena reputación (v2, v4, v8, v10, v14)
--   - green/sin insignia: buena pero sin reconocimiento (v3, v6, v11, v12, v17)
--   - yellow/sin insignia: en riesgo (v5, v16)
--   - red/sin insignia: mala reputación (v15)
-- 
-- Los vendedores con reputación yellow o red tienen descuentos
-- en sus comisiones (ver metricas_costo.descuento_reputacion).
INSERT INTO metricas_reputacion (id_vendedor, ventas_totales_periodo, total_reclamos, total_mediaciones, total_canceladas, total_envios_incorrectos, nivel_reputacion, insignia) VALUES 
(1, 1500, 5, 0, 2, 0, 'green', 'platinum'),
(2, 450, 2, 0, 1, 0, 'green', 'gold'),
(3, 120, 1, 0, 0, 0, 'green', NULL),
(4, 800, 3, 1, 5, 1, 'green', 'gold'),
(5, 300, 15, 2, 8, 2, 'yellow', NULL),
(6, 10, 0, 0, 1, 0, 'green', NULL),
(7, 2100, 8, 0, 4, 1, 'green', 'platinum'),
(8, 600, 1, 0, 2, 0, 'green', 'gold'),
(9, 1100, 4, 1, 3, 0, 'green', 'platinum'),
(10, 340, 0, 0, 0, 0, 'green', 'gold'),
(11, 200, 2, 0, 1, 0, 'green', NULL),
(12, 150, 0, 0, 0, 0, 'green', NULL),
(13, 3000, 10, 1, 5, 0, 'green', 'platinum'),
(14, 500, 1, 0, 1, 0, 'green', 'gold'),
(15, 80, 5, 2, 4, 1, 'red', NULL),
(16, 950, 20, 4, 10, 2, 'yellow', NULL),
(17, 45, 0, 0, 0, 0, 'green', NULL),
(18, 4500, 12, 1, 8, 1, 'green', 'platinum');


-- ==============================================================================
-- 4. INSERCIÓN DE MÉTRICAS DE NEGOCIO (18 registros)
-- ==============================================================================
-- Métricas comerciales clave por vendedor.
-- 
-- Consistencias internas verificadas:
--   precio_promedio_unidad = ventas_brutas_moneda_local / unidades_vendidas
--   precio_promedio_venta  = ventas_brutas_moneda_local / ventas_concretadas
--   ventas_concretadas     = ventas_totales_periodo (en metricas_reputacion)
-- 
-- Las tasas de cambio implícitas reflejan los valores de mercado de 2023:
--   ARS/USD ~357, MXN/USD ~18, BRL/USD ~5, COP/USD ~4000, CLP/USD ~900
--   VE usa USD como moneda local, por lo que moneda_local = USD
INSERT INTO metricas_negocio (id_vendedor, fecha_inicio_periodo, fecha_fin_periodo, ventas_brutas_moneda_local, ventas_brutas_usd, unidades_vendidas, visitas_totales, intencion_compra, ventas_concretadas, precio_promedio_unidad, precio_promedio_venta) VALUES 
(1, '2023-10-01', '2023-10-31', 1500000.00, 4200.00, 1550, 45000, 1800, 1500, 967.74, 1000.00),
(2, '2023-10-01', '2023-10-31', 450000.00, 1260.00, 480, 15000, 500, 450, 937.50, 1000.00),
(3, '2023-10-01', '2023-10-31', 240000.00, 670.00, 125, 8000, 150, 120, 1920.00, 2000.00),
(4, '2023-10-01', '2023-10-31', 800000.00, 45000.00, 850, 30000, 900, 800, 941.17, 1000.00),
(5, '2023-10-01', '2023-10-31', 450000.00, 25000.00, 320, 12000, 350, 300, 1406.25, 1500.00),
(6, '2023-10-01', '2023-10-31', 15000.00, 850.00, 12, 500, 15, 10, 1250.00, 1500.00),
(7, '2023-10-01', '2023-10-31', 210000.00, 42000.00, 2200, 60000, 2500, 2100, 95.45, 100.00),
(8, '2023-10-01', '2023-10-31', 90000.00, 18000.00, 650, 25000, 700, 600, 138.46, 150.00),
(9, '2023-10-01', '2023-10-31', 220000.00, 44000.00, 1150, 35000, 1300, 1100, 191.30, 200.00),
(10, '2023-10-01', '2023-10-31', 1700000.00, 420.00, 380, 10000, 400, 340, 4473.68, 5000.00),
(11, '2023-10-01', '2023-10-31', 2000000.00, 500.00, 210, 6000, 220, 200, 9523.80, 10000.00),
(12, '2023-10-01', '2023-10-31', 1200000.00, 300.00, 160, 4000, 180, 150, 7500.00, 8000.00),
(13, '2023-10-01', '2023-10-31', 45000000.00, 50000.00, 3200, 80000, 3500, 3000, 14062.50, 15000.00),
(14, '2023-10-01', '2023-10-31', 7500000.00, 8300.00, 550, 18000, 600, 500, 13636.36, 15000.00),
(15, '2023-10-01', '2023-10-31', 16000000.00, 17700.00, 85, 5000, 100, 80, 188235.29, 200000.00),
(16, '2023-10-01', '2023-10-31', 190000.00, 190000.00, 980, 40000, 1100, 950, 193.87, 200.00),
(17, '2023-10-01', '2023-10-31', 2250.00, 2250.00, 50, 1500, 60, 45, 45.00, 50.00),
(18, '2023-10-01', '2023-10-31', 3150000.00, 3150000.00, 4600, 120000, 5000, 4500, 684.78, 700.00);


-- ==============================================================================
-- 5. INSERCIÓN DE MÉTRICAS DE COSTO (18 registros)
-- ==============================================================================
-- Desglose de comisiones y costos que ML descuenta de las ventas.
-- 
-- Fórmula: neto_recibido = ventas_cobradas_total - cargos_por_venta
--                          - costos_envio - inversion_ads - otros_cargos
--                          - cargos_envio_full - descuento_reputacion
-- 
-- Casos especiales:
--   - v5 (yellow): descuento_reputacion = 17500 (penalización por reputación en riesgo)
--   - v15 (red): descuento_reputacion = 800000 (penalización por mala reputación)
--   - v7 (BR, Full): costos_envio = 0 porque usa Full, pero paga cargos_envio_full
--   - v3, v6: sin inversión en ads (inversion_ads = 0)
INSERT INTO metricas_costo (id_vendedor, ventas_cobradas_total, neto_recibido, cargos_por_venta, costos_envio, inversion_ads, otros_cargos, cargos_envio_full, descuento_reputacion) VALUES 
(1, 1500000.00, 1100000.00, 225000.00, 100000.00, 50000.00, 5000.00, 20000.00, 0.00),
(2, 450000.00, 330000.00, 67500.00, 40000.00, 10000.00, 2500.00, 0.00, 0.00),
(3, 240000.00, 180000.00, 36000.00, 20000.00, 0.00, 4000.00, 0.00, 0.00),
(4, 800000.00, 580000.00, 120000.00, 60000.00, 30000.00, 10000.00, 0.00, 0.00),
(5, 450000.00, 290000.00, 67500.00, 50000.00, 20000.00, 5000.00, 0.00, 17500.00),
(6, 15000.00, 11000.00, 2250.00, 1500.00, 0.00, 250.00, 0.00, 0.00),
(7, 210000.00, 150000.00, 31500.00, 0.00, 15000.00, 3500.00, 10000.00, 0.00),
(8, 90000.00, 65000.00, 13500.00, 8000.00, 2000.00, 1500.00, 0.00, 0.00),
(9, 220000.00, 160000.00, 33000.00, 15000.00, 8000.00, 4000.00, 0.00, 0.00),
(10, 1700000.00, 1250000.00, 255000.00, 150000.00, 30000.00, 15000.00, 0.00, 0.00),
(11, 2000000.00, 1400000.00, 300000.00, 200000.00, 50000.00, 50000.00, 0.00, 0.00),
(12, 1200000.00, 850000.00, 180000.00, 120000.00, 20000.00, 30000.00, 0.00, 0.00),
(13, 45000000.00, 32000000.00, 6750000.00, 4000000.00, 1500000.00, 750000.00, 0.00, 0.00),
(14, 7500000.00, 5500000.00, 1125000.00, 500000.00, 200000.00, 175000.00, 0.00, 0.00),
(15, 16000000.00, 10500000.00, 2400000.00, 1500000.00, 500000.00, 300000.00, 0.00, 800000.00),
(16, 190000.00, 125000.00, 28500.00, 20000.00, 10000.00, 6500.00, 0.00, 0.00),
(17, 2250.00, 1600.00, 337.50, 200.00, 50.00, 62.50, 0.00, 0.00),
(18, 3150000.00, 2300000.00, 472500.00, 200000.00, 120000.00, 57500.00, 0.00, 0.00);


-- ==============================================================================
-- 6. INSERCIÓN DE MÉTRICAS DE STOCK FULL (18 registros)
-- ==============================================================================
-- Métricas del programa Full de ML (logística administrada).
-- Los vendedores con 0 en espacios no participan en Full.
-- 
-- El puntaje_calidad indica qué tan bien está el inventario:
--   >90 = excelente, 70-90 = bueno, <70 = necesita mejora
-- El vendedor 3 no participa en Full (todos sus valores son 0).
INSERT INTO metricas_stock_full (id_vendedor, espacios_p_asignados, espacios_g_asignados, puntaje_calidad, productos_no_aptos_venta, productos_sin_rotacion, productos_antiguedad, productos_exceso_proyeccion) VALUES 
(1, 100, 20, 95, 2, 5, 0, 10),
(2, 50, 10, 85, 0, 12, 3, 5),
(3, 0, 0, 60, 0, 0, 0, 0), -- Vendedor sin envíos Full (no participa en el programa)
(4, 200, 50, 92, 5, 20, 2, 15),
(5, 150, 40, 78, 10, 45, 12, 30),
(6, 10, 2, 99, 0, 1, 0, 0),
(7, 500, 100, 98, 1, 8, 0, 20),
(8, 80, 15, 88, 3, 10, 1, 8),
(9, 120, 30, 90, 4, 15, 2, 12),
(10, 60, 10, 94, 0, 5, 0, 5),
(11, 40, 5, 82, 1, 8, 2, 4),
(12, 30, 5, 85, 0, 3, 0, 2),
(13, 800, 150, 97, 12, 40, 5, 60),
(14, 150, 20, 91, 2, 15, 1, 10),
(15, 20, 5, 65, 5, 10, 4, 8),
(16, 250, 60, 75, 15, 50, 18, 40),
(17, 15, 2, 89, 0, 2, 0, 1),
(18, 1000, 200, 96, 8, 35, 2, 80);


-- ==============================================================================
-- 7. INSERCIÓN DE MÉTRICAS DE MI PÁGINA (18 registros)
-- ==============================================================================
-- Indica qué elementos de personalización tiene configurado cada vendedor
-- en su página oficial de Mercado Libre.
-- 
-- Una página completa (banner + logo + carruseles + categorías) transmite
-- mayor profesionalismo y suele tener mejor tasa de conversión.
-- Los vendedores 5, 12 y 17 no tienen nada configurado.
INSERT INTO metricas_mi_pagina (id_vendedor, tiene_banner, tiene_logo, tiene_carruseles, categorias_organizadas) VALUES 
(1, true, true, true, true),
(2, true, true, false, true),
(3, false, true, false, false),
(4, true, true, true, true),
(5, false, false, false, false),
(6, true, true, false, false),
(7, true, true, true, true),
(8, true, true, true, false),
(9, true, true, false, true),
(10, false, true, false, false),
(11, true, false, false, true),
(12, false, false, false, false),
(13, true, true, true, true),
(14, true, true, false, true),
(15, false, true, false, false),
(16, true, true, true, true),
(17, false, false, false, false),
(18, true, true, true, true);


-- ==============================================================================
-- 8. INSERCIÓN DE RENDIMIENTO DE PUBLICACIONES (25 registros)
-- ==============================================================================
-- Un registro por cada publicación (25 total).
-- Las ventas de cada publicación suman al total de ventas_concretadas
-- del vendedor correspondiente en metricas_negocio.
-- 
-- Por ejemplo: vendedor 1 tiene 2 publicaciones (800 + 700 = 1500 ✓)
--              vendedor 18 tiene 3 publicaciones (2000 + 1500 + 1000 = 4500 ✓)
-- 
-- La relación visitas/ventas da la tasa de conversión:
--   Pub 17 (v13): 45000 visitas, 3000 ventas = 6.67% de conversión
--   Pub 5 (v4): 500 visitas, 10 ventas = 2% de conversión (baja)
INSERT INTO rendimiento_publicacion (id_publicacion, fecha_inicio_periodo, fecha_fin_periodo, visitas, ventas) VALUES 
(1, '2023-10-01', '2023-10-31', 8500, 800),
(2, '2023-10-01', '2023-10-31', 6500, 700),
(3, '2023-10-01', '2023-10-31', 12000, 450),
(4, '2023-10-01', '2023-10-31', 5000, 120),
(5, '2023-10-01', '2023-10-31', 500, 10),
(6, '2023-10-01', '2023-10-31', 9500, 790),
(7, '2023-10-01', '2023-10-31', 10000, 300),
(8, '2023-10-01', '2023-10-31', 500, 10),
(9, '2023-10-01', '2023-10-31', 30000, 2100),
(10, '2023-10-01', '2023-10-31', 7000, 350),
(11, '2023-10-01', '2023-10-31', 5000, 250),
(12, '2023-10-01', '2023-10-31', 22000, 1100),
(13, '2023-10-01', '2023-10-31', 10000, 340),
(14, '2023-10-01', '2023-10-31', 2200, 85),
(15, '2023-10-01', '2023-10-31', 3800, 115),
(16, '2023-10-01', '2023-10-31', 4000, 150),
(17, '2023-10-01', '2023-10-31', 45000, 3000),
(18, '2023-10-01', '2023-10-31', 12000, 500),
(19, '2023-10-01', '2023-10-31', 2500, 80),
(20, '2023-10-01', '2023-10-31', 18000, 450),
(21, '2023-10-01', '2023-10-31', 22000, 500),
(22, '2023-10-01', '2023-10-31', 1500, 45),
(23, '2023-10-01', '2023-10-31', 45000, 2000),
(24, '2023-10-01', '2023-10-31', 25000, 1500),
(25, '2023-10-01', '2023-10-31', 5000, 1000);


-- ==============================================================================
-- 9. INSERCIÓN DE CALIDAD DE PUBLICACIONES (25 registros)
-- ==============================================================================
-- Un registro por cada publicación con métricas de calidad.
-- 
-- El puntaje_calidad (0-100) se basa en:
--   - cantidad_fotos: más fotos = mejor (ML recomienda al menos 5)
--   - tiene_video: los videos mejoran el posicionamiento
--   - caracteristicas_completas: indica si se llenaron todos los atributos
-- 
-- Publicaciones destacadas:
--   - Pub 6 (v4, Tenis): 9 fotos, video, completo → 100 puntos
--   - Pub 17 (v13, Vino): 10 fotos, video, completo → 100 puntos
--   - Pub 23 (v18, Laptop): 10 fotos, video, completo → 100 puntos
--   - Pub 5 (v4, Zapatos): solo 2 fotos, sin video, incompleto → 45 puntos (mejorable)
INSERT INTO metricas_calidad_publicacion (id_publicacion, cantidad_fotos, tiene_video, caracteristicas_completas, puntaje_calidad) VALUES 
(1, 8, true, true, 98),
(2, 5, false, true, 85),
(3, 6, true, true, 92),
(4, 4, false, false, 70),
(5, 2, false, false, 45),
(6, 9, true, true, 100),
(7, 7, false, true, 88),
(8, 3, false, false, 60),
(9, 6, true, true, 95),
(10, 5, false, true, 82),
(11, 4, false, false, 65),
(12, 8, true, true, 96),
(13, 5, false, true, 84),
(14, 4, false, false, 72),
(15, 6, true, true, 90),
(16, 5, false, true, 85),
(17, 10, true, true, 100),
(18, 6, false, true, 88),
(19, 3, false, false, 55),
(20, 8, true, true, 97),
(21, 7, true, true, 94),
(22, 4, false, true, 78),
(23, 10, true, true, 100),
(24, 8, true, true, 95),
(25, 5, false, false, 68);


-- ==============================================================================
-- Vistas Materializadas para Diagnóstico DiME
-- ==============================================================================
-- Pre-calcula KPIs estratégicos para consumo directo desde Metabase y la API.
-- Todas las vistas incluyen COALESCE + NULLIF para evitar división por cero.
-- Se refrescan lote mediante:   REFRESH MATERIALIZED VIEW CONCURRENTLY <name>
-- ==============================================================================

-- ==============================================================================
-- 1. Reputación y Calidad
-- ==============================================================================
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_diagnostico_reputacion AS
SELECT
    v.id_vendedor,
    
    -- Fórmula: (Total de reclamos / Ventas totales del periodo) * 100
    COALESCE(
        (mr.total_reclamos::NUMERIC / NULLIF(mr.ventas_totales_periodo, 0)) * 100,
        0
    ) AS tasa_reclamos,
    
    -- Fórmula: (Total de ventas canceladas / Ventas totales del periodo) * 100
    COALESCE(
        (mr.total_canceladas::NUMERIC / NULLIF(mr.ventas_totales_periodo, 0)) * 100,
        0
    ) AS tasa_cancelaciones,
    
    -- Fórmula: (Total de mediaciones / Ventas totales del periodo) * 100
    COALESCE(
        (mr.total_mediaciones::NUMERIC / NULLIF(mr.ventas_totales_periodo, 0)) * 100,
        0
    ) AS tasa_mediaciones,
    
    -- Fórmula: (Total de envíos incorrectos / Ventas totales del periodo) * 100
    COALESCE(
        (mr.total_envios_incorrectos::NUMERIC / NULLIF(mr.ventas_totales_periodo, 0)) * 100,
        0
    ) AS tasa_envios_incorrectos,
    
    mr.nivel_reputacion,
    mr.insignia,
    mr.fecha_captura
FROM vendedor v
LEFT JOIN metricas_reputacion mr ON v.id_vendedor = mr.id_vendedor
WHERE v.esta_activo = TRUE;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_reputacion_vendedor
    ON mv_diagnostico_reputacion (id_vendedor);


-- ==============================================================================
-- 2. Ventas y Finanzas
-- ==============================================================================
-- NOTA: Crecimiento MoM requiere datos multi-período. Con la cardinalidad
-- actual 1:1 entre vendedor y metricas_negocio, retorna NULL hasta contar
-- con una serie histórica.
-- ==============================================================================
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_diagnostico_finanzas AS
SELECT
    v.id_vendedor,
    
    -- Fórmula: (Ventas concretadas / Visitas totales) * 100
    COALESCE(
        (mn.ventas_concretadas::NUMERIC / NULLIF(mn.visitas_totales, 0)) * 100,
        0
    ) AS cvr_global,
    
    -- Fórmula: (Neto recibido / Ventas brutas en moneda local) * 100
    COALESCE(
        (mc.neto_recibido / NULLIF(mn.ventas_brutas_moneda_local, 0)) * 100,
        0
    ) AS margen_neto_real,
    
    -- Fórmula: Ventas brutas en USD / Unidades vendidas
    COALESCE(
        mn.ventas_brutas_usd / NULLIF(mn.unidades_vendidas, 0),
        0
    ) AS ticket_promedio,
    
    -- Fórmula: [(Cargos por venta + Costos de envío + Inversión Ads + Cargos envío full) / Ventas brutas en moneda local] * 100
    COALESCE(
        (
            COALESCE(mc.cargos_por_venta, 0)
            + COALESCE(mc.costos_envio, 0)
            + COALESCE(mc.inversion_ads, 0)
            + COALESCE(mc.cargos_envio_full, 0)
        ) / NULLIF(mn.ventas_brutas_moneda_local, 0) * 100,
        0
    ) AS carga_total_costos,
    
    -- Fórmula: (Intención de compra / Visitas totales) * 100
    COALESCE(
        (mn.intencion_compra::NUMERIC / NULLIF(mn.visitas_totales, 0)) * 100,
        0
    ) AS ratio_intencion_compra,
    
    -- Fórmula: (Descuento por reputación / Ventas brutas en moneda local) * 100
    COALESCE(
        (mc.descuento_reputacion / NULLIF(mn.ventas_brutas_moneda_local, 0)) * 100,
        0
    ) AS descuento_reputacion,
    
    -- Fórmula: (Ventas cobradas totales / Ventas brutas en moneda local) * 100
    COALESCE(
        (mc.ventas_cobradas_total / NULLIF(mn.ventas_brutas_moneda_local, 0)) * 100,
        0
    ) AS tasa_cobro_efectivo,
    
    NULL::NUMERIC AS crecimiento_mom,
    mn.ventas_concretadas AS ventas_periodo_actual,
    mn.fecha_inicio_periodo,
    mn.fecha_fin_periodo
FROM vendedor v
LEFT JOIN metricas_negocio mn ON v.id_vendedor = mn.id_vendedor
LEFT JOIN metricas_costo mc ON v.id_vendedor = mc.id_vendedor
WHERE v.esta_activo = TRUE;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_finanzas_vendedor
    ON mv_diagnostico_finanzas (id_vendedor);


-- ==============================================================================
-- 3. Publicaciones (Calidad y Conversión Agregada)
-- ==============================================================================
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_diagnostico_publicaciones AS
SELECT
    v.id_vendedor,
    COUNT(DISTINCT p.id_publicacion) AS total_publicaciones,
    
    -- Fórmula: (Sumatoria de ventas / Sumatoria de visitas) * 100
    COALESCE(
        (SUM(rp.ventas)::NUMERIC / NULLIF(SUM(rp.visitas), 0)) * 100,
        0
    ) AS cvr_publicacion,
    
    -- Fórmula: (Cantidad de publicaciones con características completas / Total de publicaciones) * 100
    COALESCE(
        (COUNT(DISTINCT CASE WHEN mcp.caracteristicas_completas = TRUE THEN p.id_publicacion END)::NUMERIC
        / NULLIF(COUNT(DISTINCT p.id_publicacion), 0)) * 100,
        0
    ) AS pct_catalogo_completo,
    
    -- Fórmula: (Cantidad de publicaciones con video / Total de publicaciones) * 100
    COALESCE(
        (COUNT(DISTINCT CASE WHEN mcp.tiene_video = TRUE THEN p.id_publicacion END)::NUMERIC
        / NULLIF(COUNT(DISTINCT p.id_publicacion), 0)) * 100,
        0
    ) AS pct_publicaciones_con_video
FROM vendedor v
LEFT JOIN publicacion p ON v.id_vendedor = p.id_vendedor
LEFT JOIN rendimiento_publicacion rp ON p.id_publicacion = rp.id_publicacion
LEFT JOIN metricas_calidad_publicacion mcp ON p.id_publicacion = mcp.id_publicacion
WHERE v.esta_activo = TRUE
GROUP BY v.id_vendedor;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_publicaciones_vendedor
    ON mv_diagnostico_publicaciones (id_vendedor);


-- ==============================================================================
-- 4. Publicidad (Mercado Ads)
-- ==============================================================================
-- NOTA: ventas_generadas_por_ads no está disponible directamente en el esquema
-- actual. Se usa ventas_concretadas como proxy. Cuando ML exponga atribución
-- por campaña, reemplazar la fuente.
-- ==============================================================================
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_diagnostico_ads AS
SELECT
    v.id_vendedor,
    
    -- Fórmula ROAS (Return On Ad Spend): Ventas concretadas / Inversión en Ads
    CASE
        WHEN COALESCE(mc.inversion_ads, 0) > 0
        THEN COALESCE(mn.ventas_concretadas::NUMERIC / NULLIF(mc.inversion_ads, 0), 0)
        ELSE 0
    END AS roas,
    
    -- Fórmula ACOS (Advertising Cost of Sales): (Inversión en Ads / Ventas concretadas) * 100
    CASE
        WHEN COALESCE(mn.ventas_concretadas, 0) > 0
        THEN (mc.inversion_ads / NULLIF(mn.ventas_concretadas::NUMERIC, 0)) * 100
        ELSE 0
    END AS acos,
    
    -- Fórmula: (Inversión en Ads / Ventas brutas en moneda local) * 100
    COALESCE(
        (mc.inversion_ads / NULLIF(mn.ventas_brutas_moneda_local, 0)) * 100,
        0
    ) AS inversion_ads_sobre_ventas,
    
    mc.inversion_ads
FROM vendedor v
LEFT JOIN metricas_costo mc ON v.id_vendedor = mc.id_vendedor
LEFT JOIN metricas_negocio mn ON v.id_vendedor = mn.id_vendedor
WHERE v.esta_activo = TRUE;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_ads_vendedor
    ON mv_diagnostico_ads (id_vendedor);


-- ==============================================================================
-- 5. Stock Full (Logística)
-- ==============================================================================
-- NOTA: "unidades_activas_vendibles" y "total_skus_en_full" no existen como
-- columnas directas en metricas_stock_full. Se aproximan usando las columnas
-- disponibles. Cuando ML exponga el inventario detallado, reemplazar.
--
-- NOTA MATEMÁTICA: Para estas métricas, el denominador común asumido como "Total de espacios" 
-- es: (espacios_p_asignados + espacios_g_asignados)
-- ==============================================================================
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_diagnostico_stock AS
SELECT
    v.id_vendedor,
    
    -- Fórmula: [Productos sin rotación / (Espacios P + Espacios G)] * 100
    COALESCE(
        (msf.productos_sin_rotacion::NUMERIC
        / NULLIF(msf.espacios_p_asignados + msf.espacios_g_asignados, 0)) * 100,
        0
    ) AS dead_stock_rate,
    
    -- Fórmula: [Productos con antigüedad de riesgo / (Espacios P + Espacios G)] * 100
    COALESCE(
        (msf.productos_antiguedad::NUMERIC
        / NULLIF(msf.espacios_p_asignados + msf.espacios_g_asignados, 0)) * 100,
        0
    ) AS antiguedad_riesgo,
    
    -- Fórmula: [Productos no aptos para venta / (Espacios P + Espacios G)] * 100
    COALESCE(
        (msf.productos_no_aptos_venta::NUMERIC
        / NULLIF(msf.espacios_p_asignados + msf.espacios_g_asignados, 0)) * 100,
        0
    ) AS productos_no_aptos,
    
    -- Fórmula: [Productos con exceso de proyección / (Espacios P + Espacios G)] * 100
    COALESCE(
        (msf.productos_exceso_proyeccion::NUMERIC
        / NULLIF(msf.espacios_p_asignados + msf.espacios_g_asignados, 0)) * 100,
        0
    ) AS overstock_rate,
    
    -- Fórmula: [((Espacios P + Espacios G) - Productos sin rotación - Productos no aptos) / (Espacios P + Espacios G)] * 100
    COALESCE(
        GREATEST(
            ((msf.espacios_p_asignados + msf.espacios_g_asignados)
            - msf.productos_sin_rotacion
            - msf.productos_no_aptos_venta)::NUMERIC,
            0
        ) / NULLIF(msf.espacios_p_asignados + msf.espacios_g_asignados, 0) * 100,
        0
    ) AS utilizacion_espacios,
    
    msf.puntaje_calidad
FROM vendedor v
LEFT JOIN metricas_stock_full msf ON v.id_vendedor = msf.id_vendedor
WHERE v.esta_activo = TRUE;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_stock_vendedor
    ON mv_diagnostico_stock (id_vendedor);


-- Borrar las tablas(General)
    DROP TABLE IF EXISTS 
    metricas_calidad_publicacion, 
    rendimiento_publicacion, 
    metricas_mi_pagina, 
    metricas_stock_full, 
    metricas_costo, 
    metricas_negocio, 
    metricas_reputacion, 
    reportes_diagnostico, 
    publicacion, 
    vendedor, 
    plan_saas, 
    moneda, 
    pais 
CASCADE;
// --- 1. DICCIONARIOS ---
const diccionarioAcciones = {

    // --- 1. REPUTACIÓN & CALIDAD DE SERVICIO ---
    "tasa_reclamos_ROJO": "Auditar la causa raíz de los reclamos más recientes (producto, despacho, comunicación) y congelar o pausar las publicaciones con reclamos recurrentes mientras se corrige el origen.",
    "tasa_reclamos_AMARILLO": "Revisar las últimas 20 órdenes con reclamo para identificar un patrón común antes de que el indicador escale, especialmente antes de eventos de alto volumen como CyberDay.",
    "tasa_reclamos_VERDE": "Mantener el protocolo de post-venta actual sin cambios; monitorear semanalmente para detectar cualquier desviación temprana.",

    "tasa_cancelaciones_ROJO": "Auditar de inmediato el flujo de sincronización de stock y pricing automático; identificar si el origen es falta de stock, error de precio o falla logística.",
    "tasa_cancelaciones_AMARILLO": "Identificar el origen específico de las cancelaciones recientes y corregirlo antes de Fiestas Patrias o CyberDay, cuando el mayor volumen amplifica el problema.",
    "tasa_cancelaciones_VERDE": "Mantener la sincronización de inventario y precios actualizada en tiempo real como práctica estándar.",

    "tasa_mediaciones_ROJO": "Capacitar al equipo de atención en resolución proactiva de reclamos y revisar si hay reclamos abiertos sin respuesta que estén escalando por defecto.",
    "tasa_mediaciones_AMARILLO": "Reforzar el guion de respuesta a reclamos, ofreciendo una solución concreta dentro de las primeras 24 horas para evitar la escalada a mediación.",
    "tasa_mediaciones_VERDE": "Mantener tiempos de respuesta rápidos en mensajería como estándar de servicio.",

    "tasa_envios_incorrectos_ROJO": "Auditar de inmediato el proceso de despacho (picking/packing); es la causa raíz más probable detrás del deterioro de reclamos y mediaciones.",
    "tasa_envios_incorrectos_AMARILLO": "Reforzar el checklist de empaque en los SKUs de mayor rotación antes de que el problema se traduzca en un termómetro deteriorado.",
    "tasa_envios_incorrectos_VERDE": "Mantener el doble check de producto antes de despacho como parte del proceso estándar.",

    "nivel_reputacion_ROJO": "Priorizar la corrección del KPI base con peor desviación (reclamos, cancelaciones, mediaciones o envíos incorrectos) como primer paso del plan de recuperación de 60 días.",
    "nivel_reputacion_AMARILLO": "Identificar cuál KPI base está empujando el deterioro y corregirlo dentro de la ventana de 60 días antes de la siguiente reevaluación.",
    "nivel_reputacion_VERDE": "Sostener el monitoreo semanal de los KPIs base de reputación para no perder esta posición.",

    "insignia_ROJO": "Corregir primero reclamos y mediaciones (causa más probable de la pérdida de insignia) antes de evaluar cualquier otra palanca comercial.",
    "insignia_AMARILLO": "Identificar cuál de los dos requisitos (reclamos < 1% o cancelaciones < 2%) está limitando el ascenso a Platinum y priorizarlo.",
    "insignia_VERDE": "Sostener reclamos < 1% y cancelaciones < 2% de forma continua en los últimos 60 días de evaluación para no perder el nivel.",

    // --- 2. VENTAS & RENTABILIDAD ---
    "cvr_global_ROJO": "Revisar en conjunto fotos, ficha técnica, precio competitivo y estado del termómetro de reputación antes de invertir más presupuesto en tráfico pago.",
    "cvr_global_AMARILLO": "Diagnosticar si el cuello de botella está en precio, fotos o reputación antes de escalar inversión en tráfico, para no diluir el ROI agregando visitas a un funnel que aún no convierte óptimamente.",
    "cvr_global_VERDE": "Escalar inversión en tráfico (ads, eventos) con confianza, dado que el funnel ya demuestra capacidad de conversión sólida.",

    "margen_neto_real_ROJO": "1) Revisa tu termómetro de reputación - si está en rojo, resuelve los reclamos abiertos urgentemente. 2) Audita tus costos de envío: ¿estás usando Full cuando podrías usar Flex? 3) Evalúa si ofrecer cuotas sin interés vale la pena para tu ticket promedio (si es bajo, estás regalando margen). 4) Sube precios mínimo un 5-10% en los productos con mayor rotación para recuperar parte del payout perdido. No tiene sentido escalar ventas si cada venta tiene este nivel de retención.",
    "margen_neto_real_AMARILLO": "Revisa tu estructura de costos: ¿estás ofreciendo cuotas sin interés que no puedes absorber? ¿Tus envíos son más caros que el promedio de tu categoría? Considera ajustar precios un 3-5% para compensar la retención sin perder competitividad. También revisa que no tengas descuentos por reputación activos que estén aumentando tu comisión.",
    "margen_neto_real_VERDE": "Tu eficiencia en costos de plataforma es óptima. Asegúrate de mantener el termómetro en verde para no activar descuentos por reputación que podrían reducir este porcentaje. Puedes usar este colchón para invertir en mejorar la calidad de tus publicaciones o probar nuevas categorías.",
    
    "ticket_promedio_ROJO": "Pausar ads en los SKUs de ticket bajo o redirigir presupuesto hacia productos de mayor valor por transacción.",
    "ticket_promedio_AMARILLO": "Evaluar estrategias de cross-sell o bundles para elevar el ticket antes de escalar inversión adicional en publicidad.",
    "ticket_promedio_VERDE": "Usar el ticket alto como palanca para invertir en calidad de publicación y envío, evitando erosionarlo con descuentos masivos.",

    "ratio_intencion_compra_ROJO": "Revisar si el tráfico que se está atrayendo (orgánico o pago) corresponde realmente al perfil de comprador del producto publicado.",
    "ratio_intencion_compra_AMARILLO": "Revisar competitividad de precio y estado de reputación antes de invertir más en atraer tráfico adicional.",
    "ratio_intencion_compra_VERDE": "Capitalizar el interés ya generado optimizando el proceso de cierre: checkout, disponibilidad de stock y tiempos de respuesta.",
   
    "descuento_reputacion_ROJO": "Cuantificar la pérdida en CLP absolutos y usarla como argumento prioritario para enfocar recursos en mejorar el termómetro de reputación.",
    "descuento_reputacion_AMARILLO": "Monitorear la tendencia de este costo junto con los KPIs base de reputación para anticipar si va en aumento.",
    "descuento_reputacion_VERDE": "Ninguna acción requerida; confirma que el termómetro está saludable y sin fugas de margen por este concepto.",

    "tasa_cobro_efectivo_ROJO": "Revisar el estado de los reclamos activos como primera hipótesis antes de explorar otras causas de la brecha de cobro.",
    "tasa_cobro_efectivo_AMARILLO": "Conciliar el detalle de ventas no cobradas contra los reclamos abiertos para anticipar el origen de la brecha.",
    "tasa_cobro_efectivo_VERDE": "Mantener el monitoreo mensual del ciclo de liquidación sin intervención adicional.",

    "crecimiento_mom_ROJO": "Revisar en conjunto reputación, conversión y eficiencia de publicidad, dado que una caída de ingresos rara vez tiene una sola causa aislada.",
    "crecimiento_mom_VERDE": "Sostener las prácticas actuales y monitorear que el crecimiento no esté sacrificando margen o reputación en el proceso.",

    // --- 3. CALIDAD & RENDIMIENTO DE PUBLICACIONES ---
    "puntaje_calidad_ROJO": "Revisar título, atributos y multimedia de las publicaciones con peor puntaje, priorizando las de mayor potencial de tráfico, antes de invertir en ads.",
    "puntaje_calidad_AMARILLO": "Identificar qué atributo específico falta (fotos, características, descripción) para cruzar el umbral de prioridad algorítmica.",
    "puntaje_calidad_VERDE": "Mantener revisión periódica de título, atributos y multimedia para sostener la prioridad de búsqueda ya alcanzada.",

    "cvr_publicacion_ROJO": "Auditar la publicación (precio, fotos, ficha) o darla de baja si tras la corrección no mejora, para no seguir afectando el score general de la cuenta.",
    "cvr_publicacion_AMARILLO": "Revisar fotos, precio y ficha técnica de la publicación antes de asignarle presupuesto adicional de ads.",
    "cvr_publicacion_VERDE": "Priorizar esta publicación para inversión adicional en ads, dado que el funnel ya demostró capacidad de conversión.",

    "pct_catalogo_completo_ROJO": "Completar las características técnicas faltantes priorizando los SKUs de mayor tráfico, para recuperar presencia en filtros de búsqueda lo antes posible.",
    "pct_catalogo_completo_AMARILLO": "Completar la ficha técnica del catálogo restante, comenzando por las categorías donde los compradores filtran con mayor frecuencia.",
    "pct_catalogo_completo_VERDE": "Mantener el estándar de ficha completa exigiéndolo en cada publicación nueva que se agregue al catálogo.",

    "pct_publicaciones_con_video_ROJO": "Priorizar la incorporación de video en las publicaciones de mayor tráfico, donde el impacto en conversión es más alto.",
    "pct_publicaciones_con_video_AMARILLO": "Ampliar gradualmente la cobertura de video hacia más categorías del catálogo activo.",
    "pct_publicaciones_con_video_VERDE": "Mantener la incorporación de video como estándar en publicaciones nuevas o relanzadas.",

    // --- 4. PUBLICIDAD - PRODUCT ADS ---
    "roas_ROJO": "Pausar o reestructurar de inmediato las campañas con este nivel de retorno antes de seguir comprometiendo presupuesto.",
    "roas_AMARILLO": "Confirmar que el objetivo declarado de la campaña (crecimiento o defensa de categoría) justifica este nivel, y monitorear que no se acerque a 3x.",
    "roas_VERDE": "Evaluar escalar presupuesto manteniendo este nivel de retorno, especialmente de cara a eventos de alto tráfico como CyberDay.",

    "acos_ROJO": "Recalcular el objetivo de campaña usando la regla ACoS sostenible, y ajustar pujas en consecuencia.",
    "acos_AMARILLO": "Recalcular este nivel contra el margen bruto real de la cuenta para confirmar que la estrategia de crecimiento sigue siendo sostenible.",
    "acos_VERDE": "Mantener el nivel actual de inversión publicitaria, alineado con el objetivo de rentabilidad de la cuenta.",

    "inversion_ads_sobre_ventas_ROJO": "Evaluar si el tráfico orgánico (puntaje de calidad, reputación) puede asumir parte de la carga actual sostenida por ads, antes de seguir escalando inversión.",
    "inversion_ads_sobre_ventas_AMARILLO": "Revisar si hay margen de mejora en tráfico orgánico para reducir gradualmente la dependencia de publicidad.",
    "inversion_ads_sobre_ventas_VERDE": "Mantener el uso de ads como acelerador de crecimiento orgánico, no como sostén principal de ventas.",

    // --- 5. STOCK FULL ---
    "dead_stock_rate_ROJO": "Auditar de inmediato el catálogo para definir qué SKUs liquidar, promocionar o retirar de Full.",
    "dead_stock_rate_AMARILLO": "Identificar ahora los SKUs sin movimiento, antes de que crucen los 30 días en Full y empiecen a generar cargos por antigüedad.",
    "dead_stock_rate_VERDE": "Mantener el monitoreo semanal de rotación de inventario en Full.",

    "antiguedad_riesgo_ROJO": "Aplicar liquidación, descuento agresivo o retiro de bodega sobre los SKUs específicos que ya están generando cargos.",
    "antiguedad_riesgo_AMARILLO": "Planificar promociones de liquidación para los SKUs en este tramo antes de que generen cargos diarios.",
    "antiguedad_riesgo_VERDE": "Mantener el ciclo de revisión semanal de antigüedad de inventario en Full.",

    "productos_no_aptos_ROJO": "Revisar el proceso de empaque y la calidad del proveedor de inmediato, dado que este KPI tiene como único umbral ideal el 0%.",
    "productos_no_aptos_AMARILLO": "Identificar si los casos se concentran en un proveedor o transportista específico antes de que se vuelvan recurrentes.",
    "productos_no_aptos_VERDE": "Mantener el estándar de calidad de empaque y envío a bodega actual.",

    "overstock_rate_ROJO": "Recalcular las proyecciones de reposición antes del próximo envío a Full para alinear stock con demanda real.",
    "overstock_rate_AMARILLO": "Ajustar a la baja el próximo ciclo de reposición en los SKUs identificados como excedidos.",
    "overstock_rate_VERDE": "Mantener el ciclo de reposición actual, ajustado a 30–60 días de cobertura.",

    "utilizacion_espacios_ROJO": "Si es baja, evaluar ampliar el catálogo activo en Full; si es alta, liberar espacio para reducir riesgo de quiebre en productos estrella.",
    "utilizacion_espacios_AMARILLO": "Evaluar ampliar el catálogo activo en Full para aprovechar la capacidad asignada no utilizada.",
    "utilizacion_espacios_VERDE": "Mantener la asignación actual de espacio, que ya está en zona óptima de uso productivo.",

    // --- 6. MI PÁGINA & PRESENCIA DE TIENDA ---
    "tiene_banner_ROJO": "Instalar banner profesional como acción prioritaria; es uno de los cambios de menor costo y mayor impacto en confianza del comprador.",
    "tiene_banner_AMARILLO": "Actualizar el banner para alinearlo con la campaña o temporada vigente en el próximo ciclo de campaña.",
    "tiene_banner_VERDE": "Mantener el banner actualizado en cada cambio relevante de temporada o campaña.",

    "tiene_logo_ROJO": "Instalar el logo de marca como elemento mínimo de diferenciación visual frente a otros vendedores de la categoría.",
    "tiene_logo_AMARILLO": "Alinear el logo con la identidad visual usada en otros canales de la marca para reforzar reconocimiento.",
    "tiene_logo_VERDE": "Mantener la consistencia visual del logo en toda la presencia de 'Mi Página'.",

    "tiene_carruseles_ROJO": "Activar los carrousels de productos junto con la organización de categorías, dado que ambos elementos se refuerzan mutuamente en la experiencia de navegación.",
    "tiene_carruseles_AMARILLO": "Ampliar los carrousels a las categorías de mayor margen para capturar más oportunidades de cross-sell.",
    "tiene_carruseles_VERDE": "Mantener los carrousels actualizados con las novedades y productos de mayor rotación del catálogo.",

    "categorias_organizadas_ROJO": "Reorganizar categorías priorizando las líneas de producto de mayor tráfico, en paralelo a la activación de carruseles.",
    "categorias_organizadas_AMARILLO": "Completar la organización de categorías en las líneas de producto con mayor tráfico restante.",
    "categorias_organizadas_VERDE": "Mantener la estructura de categorías actualizada a medida que se incorporan nuevas líneas de producto."
};

const planesIntegrados = [
    // --- COMBINACIONES DE REPUTACIÓN ---
    {
        nombre: "Falla Logística Crítica",
        prioridad: "Urgente",
        condiciones: [ ["tasa_reclamos_ROJO"], ["tasa_envios_incorrectos_ROJO"] ],
        accion: "1) Auditar el proceso de picking/packing como prioridad uno. 2) Recién después, ajustar el guion de atención al comprador — atacar primero la causa logística evita corregir solo el síntoma."
    },
    {
        nombre: "Problemas de Atención sin Impacto Logístico",
        prioridad: "Urgente",
        condiciones: [ ["tasa_mediaciones_ROJO"], ["tasa_cancelaciones_VERDE"] ],
        accion: "1) Reforzar tiempos y calidad de respuesta a reclamos abiertos. 2) No tocar procesos de stock/pricing, que ya están funcionando correctamente."
    },
    {
        nombre: "Pérdida de Insignia por Reclamos",
        prioridad: "Urgente",
        condiciones: [ ["nivel_reputacion_ROJO"], ["insignia_ROJO"], ["tasa_reclamos_ROJO"] ],
        accion: "1) Plan de recuperación de 60 días enfocado exclusivamente en bajar reclamos por debajo de 1.25%. 2) Pausar cualquier inversión en crecimiento de tráfico hasta ver mejora en el termómetro, ya que el tráfico adicional no se traducirá en ventas mientras la visibilidad esté penalizada."
    },

    // --- COMBINACIONES DE VENTAS & RENTABILIDAD ---
    {
        nombre: "Colapso de Conversión y Costos",
        prioridad: "Urgente",
        condiciones: [ ["cvr_global_ROJO"], ["carga_total_costos_ROJO"], ["margen_neto_real_ROJO"] ],
        accion: "1) Pausar cualquier escalamiento de tráfico o ads. 2) Resolver primero conversión (fotos, ficha, precio) y estructura de costos. 3) Solo después de estabilizar ambos frentes, evaluar inversión de crecimiento — invertir en tráfico mientras el funnel y el costo están rotos agrava la pérdida."
    },
    {
        nombre: "Penalización de Rentabilidad por Reputación",
        prioridad: "Urgente",
        condiciones: [ ["margen_neto_real_ROJO"], ["descuento_reputacion_ROJO"] ],
        accion: "1) Resolver reputación antes de tocar pricing. 2) Recalcular el margen objetivo una vez eliminada la penalización, para no optimizar precios sobre una base de costos distorsionada."
    },
    {
        nombre: "Estancamiento de Ventas con Brecha de Cobro",
        prioridad: "Urgente",
        condiciones: [ ["crecimiento_mom_ROJO"], ["tasa_cobro_efectivo_AMARILLO", "tasa_cobro_efectivo_ROJO"] ], // Soporta Amarillo o Rojo
        accion: "1) Resolver los reclamos abiertos como prioridad de caja inmediata. 2) Una vez liberado el cobro retenido, evaluar palancas de crecimiento de ventas, ya que mientras haya reclamos abiertos cualquier ganancia de ventas seguirá parcialmente retenida."
    },

    // --- COMBINACIONES DE CALIDAD & RENDIMIENTO DE PUBLICACIONES ---
    {
        nombre: "Falla de Conversión Pura en Publicación",
        prioridad: "Urgente",
        // Aquí no dependemos de "Tráfico normal" porque no existe en la BD, la tracción principal es la conversión rota.
        condiciones: [ ["cvr_publicacion_ROJO"] ],
        accion: "1) Enfocar la corrección directamente en la página de publicación (multimedia, precio, descripción). 2) No aumentar inversión de ads sobre esta publicación hasta confirmar mejora en conversión, ya que más tráfico sobre un funnel roto solo amplifica la pérdida."
    },
    {
        nombre: "Déficit Total de Calidad Multimedia",
        prioridad: "Urgente",
        // Adaptado: Se omitió cobertura_fotos porque no figura en la base de datos entregada.
        condiciones: [ ["pct_publicaciones_con_video_ROJO"], ["puntaje_calidad_ROJO"] ],
        accion: "1) Plan de re-fotografía y video en lote para el catálogo completo, priorizando SKUs de mayor tráfico potencial. 2) Es el ajuste de mayor retorno disponible dado que corrige simultáneamente visibilidad algorítmica y conversión directa."
    },
    {
        nombre: "Caída de Conversión por Ficha Incompleta",
        prioridad: "Urgente",
        condiciones: [ ["pct_catalogo_completo_ROJO"], ["cvr_publicacion_ROJO"] ],
        accion: "1) Priorizar completar ficha técnica antes de invertir en ads, ya que el tráfico pagado se perdería en el mismo cuello de botella de conversión. 2) Una vez completada la ficha, reevaluar si el CVR mejora antes de asignar presupuesto adicional."
    },

    // --- COMBINACIONES DE PUBLICIDAD ---
    {
        nombre: "Quema de Presupuesto Ineficiente",
        prioridad: "Urgente",
        condiciones: [ ["roas_ROJO"], ["inversion_ads_sobre_ventas_ROJO"] ],
        accion: "1) Pausar de inmediato las campañas de menor ROAS. 2) Recalcular el ACoS objetivo sobre el margen bruto real antes de reactivar cualquier campaña. 3) No reanudar inversión hasta confirmar que el retorno proyectado supera el umbral de rentabilidad mínimo."
    },

    // --- COMBINACIONES DE STOCK FULL ---
    {
        nombre: "Acumulación Crítica de Cargos Full",
        prioridad: "Urgente",
        condiciones: [ ["dead_stock_rate_ROJO"], ["antiguedad_riesgo_ROJO"] ],
        accion: "1) Priorizar liquidación por antigüedad: los SKUs más viejos primero, para frenar la acumulación de cargos diarios. 2) Una vez controlados los cargos activos, atacar el resto del dead stock según rotación histórica."
    },
    {
        nombre: "Colapso de Espacio por Mala Proyección",
        prioridad: "Urgente",
        condiciones: [ ["overstock_rate_ROJO"], ["utilizacion_espacios_ROJO"] ],
        accion: "1) Redistribuir capacidad de Full: liberar espacio de los SKUs sobrestockeados. 2) Reasignar ese espacio liberado a los productos de mayor rotación que están en riesgo de quiebre."
    },
    {
        nombre: "Capacidad Full Desaprovechada",
        prioridad: "Preventiva",
        condiciones: [ ["utilizacion_espacios_ROJO"], ["dead_stock_rate_VERDE"] ],
        accion: "1) Evaluar ampliar el catálogo activo en Full, dado que el inventario actual ya está sano. 2) No auditar el inventario existente como primera acción, ya que el problema es de capacidad ociosa, no de gestión."
    },

    // --- COMBINACIONES DE MI PÁGINA & PRESENCIA DE TIENDA ---
    {
        nombre: "Ausencia de Marca Mínima Viable",
        prioridad: "Urgente",
        condiciones: [ ["tiene_banner_ROJO"], ["tiene_logo_VERDE"] ],
        accion: "1) Instalar banner como complemento directo al logo ya presente. 2) Es la pieza faltante de menor costo dentro de la identidad de marca actual."
    },
    {
        nombre: "Navegación Rota en Tienda",
        prioridad: "Urgente",
        condiciones: [ ["tiene_carruseles_ROJO"], ["categorias_organizadas_ROJO"] ],
        accion: "1) Activar carrousels y reorganizar categorías en el mismo ciclo de trabajo. 2) Priorizar las categorías de mayor tráfico para maximizar el impacto inmediato en navegación."
    },
    {
        nombre: "Priorización de Reputación vs. Estética",
        prioridad: "Urgente",
        condiciones: [ ["tiene_banner_ROJO"], ["tiene_logo_ROJO"], ["tiene_carruseles_ROJO"], ["categorias_organizadas_ROJO"], ["nivel_reputacion_ROJO"] ],
        accion: "1) Priorizar primero la recuperación del termómetro de reputación, dado su mayor impacto en visibilidad. 2) En paralelo, instalar banner y logo como señales rápidas de profesionalismo mientras se resuelve la reputación, ya que son acciones de bajo costo y ejecución inmediata."
    }
];

// --- 2. TRADUCTOR DE NOMBRES ---
// Convierte lo que manda el backend ("Tasa de Conversión Global (CVR)") a nuestra llave ("cvr_global")
function obtenerLlaveBase(nombreKpi) {
    // Convertimos a minúsculas para evaluar más fácil
    const n = nombreKpi.toLowerCase();
    
    // ESPECÍFICOS PRIMERO (Para evitar que choquen)
    if (n.includes("descuento")) return "descuento_reputacion";
    if (n.includes("cvr por publicación") || (n.includes("cvr") && n.includes("publicación"))) return "cvr_publicacion";
    
    // REPUTACIÓN (Buscamos con y sin tilde)
    if (n.includes("reputación") || n.includes("reputacion") || n.includes("termómetro") || n.includes("termometro") || n.includes("nivel")) return "nivel_reputacion";
    
    if (n.includes("reclamos")) return "tasa_reclamos";
    if (n.includes("cancelaciones")) return "tasa_cancelaciones";
    if (n.includes("mediaciones")) return "tasa_mediaciones";
    if (n.includes("incorrectos")) return "tasa_envios_incorrectos";
    if (n.includes("insignia")) return "insignia";
    
    // VENTAS & FINANZAS
    if (n.includes("conversión") || n.includes("conversion") || n.includes("cvr")) return "cvr_global"; 
    if (n.includes("margen")) return "margen_neto_real";
    if (n.includes("ticket") || n.includes("aov")) return "ticket_promedio";
    if (n.includes("carga") || n.includes("costos")) return "carga_total_costos";
    if (n.includes("intención") || n.includes("intencion")) return "ratio_intencion_compra";
    if (n.includes("cobro")) return "tasa_cobro_efectivo";
    if (n.includes("crecimiento")) return "crecimiento_mom";
    
    // CALIDAD & RENDIMIENTO
    if (n.includes("puntaje") || n.includes("calidad")) return "puntaje_calidad";
    if (n.includes("cobertura") || n.includes("fotos")) return "cobertura_fotos";
    if (n.includes("catálogo") || n.includes("catalogo") || n.includes("características")) return "pct_catalogo_completo";
    if (n.includes("video")) return "pct_publicaciones_con_video";
    
    // PUBLICIDAD
    if (n.includes("roas")) return "roas";
    if (n.includes("acos")) return "acos";
    if (n.includes("inversión") || n.includes("inversion")) return "inversion_ads_sobre_ventas";
    
    // LOGÍSTICA
    if (n.includes("dead stock") || n.includes("rotación") || n.includes("rotacion")) return "dead_stock_rate";
    if (n.includes("antigüedad") || n.includes("antiguedad") || n.includes("riesgo")) return "antiguedad_riesgo";
    if (n.includes("aptos")) return "productos_no_aptos";
    if (n.includes("overstock") || n.includes("exceso")) return "overstock_rate";
    if (n.includes("espacios") || n.includes("utilización") || n.includes("utilizacion")) return "utilizacion_espacios";
    
    // PRESENCIA DE TIENDA
    if (n.includes("banner")) return "tiene_banner";
    if (n.includes("logo")) return "tiene_logo";
    if (n.includes("carrusel") || n.includes("carrousel")) return "tiene_carruseles";
    if (n.includes("categorías") || n.includes("categorias")) return "categorias_organizadas";
    
    return "desconocido";
}

// --- 3. LÓGICA PRINCIPAL ---

// --- FUNCIÓN AUXILIAR PARA EL LOGO ---
async function cargarImagenComoBase64(url) {
    try {
        const response = await fetch(url);
        const blob = await response.blob();
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    } catch (e) {
        console.warn("No se pudo cargar el logo para el PDF", e);
        return null;
    }
}


// TRADUCTOR DE COLORES (Inglés a Español)
function normalizarSemaforo(estado) {
    if (!estado) return "GRIS";
    
    const e = String(estado).toUpperCase().trim();
    
    // Si viene en inglés o español, lo forzamos a nuestro diccionario
    if (e === "RED" || e === "ROJO") return "ROJO";
    if (e === "YELLOW" || e === "AMARILLO") return "AMARILLO";
    if (e === "GREEN" || e === "VERDE") return "VERDE";
    
    return "GRIS";
}

// --- 3. LÓGICA PRINCIPAL ---
document.addEventListener('DOMContentLoaded', () => {
    const btnGenerar = document.getElementById('btn-generate-plan');
    
    if (!btnGenerar) return;

    btnGenerar.addEventListener('click', async () => {
        try {
            btnGenerar.innerText = "⏳ Auditando métricas y generando PDF...";
            btnGenerar.style.pointerEvents = "none";
            
            const token = localStorage.getItem('access_token');
            const vendedorId = localStorage.getItem('vendedor_id') || 1; 
            
            if (!vendedorId) {
                alert("Error: Sesión de vendedor no encontrada.");
                return;
            }

            const headers = {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''
            };

            const response = await fetch(`/api/kpis-query?vendedor_id=${vendedorId}`, { headers });
            if (!response.ok) throw new Error("Fallo en la comunicación con el servidor.");
            
            const dataKpis = await response.json();
            
            const firmasActuales = new Set();
            dataKpis.items.forEach(kpi => {
                const llaveBase = obtenerLlaveBase(kpi.nombre_kpi);
                const semaforoReal = normalizarSemaforo(kpi.estado_semaforo);
                firmasActuales.add(`${llaveBase}_${semaforoReal}`);
            });
            
            let planFinal = [];
            let kpisProcesadosEnCombinacion = new Set();

            // Evaluar Combinaciones
            planesIntegrados.forEach(plan => {
                const aplicaCombinacion = plan.condiciones.every(grupoCondiciones => 
                    grupoCondiciones.some(condicion => firmasActuales.has(condicion))
                );
                
                if (aplicaCombinacion) {
                    planFinal.push({
                        titulo: plan.nombre,
                        prioridad: plan.prioridad,
                        accion: plan.accion,
                        valorActual: "Múltiples métricas afectadas",
                        dimension: "Estrategia Cruzada", // Asignamos una dimensión genérica
                        semaforo: "ROJO" // Las combinaciones siempre son críticas
                    });
                    
                    plan.condiciones.forEach(grupo => {
                        grupo.forEach(c => kpisProcesadosEnCombinacion.add(c));
                    });
                }
            });

            // Evaluar KPIs Individuales
            dataKpis.items.forEach(kpi => {
                const llaveBase = obtenerLlaveBase(kpi.nombre_kpi);

                if (llaveBase === "carga_total_costos") {
                    return; 
                }

                const semaforoReal = normalizarSemaforo(kpi.estado_semaforo);
            
                const firma = `${llaveBase}_${semaforoReal}`; 

                
                // Evaluamos que no esté en una combinación procesada
                if ((semaforoReal === 'ROJO' || semaforoReal === 'AMARILLO' || semaforoReal === 'VERDE') && !kpisProcesadosEnCombinacion.has(firma)) {
                    
                    const accionRecomendada = diccionarioAcciones[firma] || `Requiere atención en el módulo de ${kpi.dimension || 'correspondiente'}.`;
                    
                    let tituloMostrar = kpi.nombre_kpi;
                    if (llaveBase === "margen_neto_real") {
                        tituloMostrar = "Payout Rate";
                    }

                    planFinal.push({
                        titulo: tituloMostrar,
                       // titulo: kpi.nombre_kpi, 
                        prioridad: kpi.prioridad || "Atención", 
                        accion: accionRecomendada,
                        valorActual: kpi.valor_actual || "N/A",
                        dimension: kpi.dimension || "Otros",
                        semaforo: semaforoReal
                    });
                }
            }); // 

            // Agrupar por Dimensión (Logística, Reputación, etc.)
            const planesAgrupados = planFinal.reduce((acc, item) => {
                if (!acc[item.dimension]) acc[item.dimension] = [];
                acc[item.dimension].push(item);
                return acc;
            }, {});

            // Cargar el Logo en Base64 antes de dibujar el PDF
            const logoBase64 = await cargarImagenComoBase64('/assets/images/DiME_Logo_Inverso.png');

            // --- DISEÑO DEL PDF MINIMALISTA ---
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            // 1. Cabecera Elegante
            doc.setFillColor(15, 23, 42); // Azul oscuro DiME
            doc.rect(0, 0, 210, 32, 'F');
            
            if (logoBase64) {
                doc.addImage(logoBase64, 'PNG', 15, 8, 50, 15); 
            } else {
                // Respaldo por si falla la imagen
                doc.setTextColor(255, 255, 255);
                doc.setFontSize(16);
                doc.setFont("helvetica", "bold");
                doc.text("DiME", 15, 20);
            }

            // Título alineado a la derecha
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(14);
            doc.setFont("helvetica", "normal");
            doc.text("Plan de Acción Estratégico", 195, 20, { align: "right" });
            
            let y = 45;
            
            if (planFinal.length === 0) {
                doc.setTextColor(21, 128, 61); 
                doc.setFontSize(12);
                doc.text("¡Felicidades! Todos tus indicadores están en niveles óptimos de optimización.", 15, y);
            } else {
                // Iterar sobre cada sección agrupada
                Object.keys(planesAgrupados).forEach(dimension => {
                    // Control de salto de página para nuevas secciones
                    if (y > 250) {
                        doc.addPage();
                        y = 20;
                    }

                    // Título de la Dimensión (Fondo gris tenue)
                    doc.setFillColor(241, 245, 249); // Slate 100
                    doc.rect(15, y, 180, 10, 'F');
                    doc.setTextColor(30, 41, 59); // Slate 800
                    doc.setFontSize(11);
                    doc.setFont("helvetica", "bold");
                    doc.text(dimension.toUpperCase(), 20, y + 7);
                    
                    y += 20;

                    // Iterar sobre las acciones de esta dimensión
                    planesAgrupados[dimension].forEach(item => {
                        if (y > 265) {
                            doc.addPage();
                            y = 20;
                        }
                        
                        // Determinar el color del semáforo
                        let colorHex = [202, 138, 4]; // Amarillo por defecto (Amber 600)
                        if (item.semaforo === 'ROJO' || item.prioridad.toUpperCase().includes('URGENTE') || item.titulo.toUpperCase().includes('CRÍTICO')) {
                            colorHex = [220, 38, 38]; // Rojo (Red 600)
                        } else if (item.semaforo === 'VERDE') {
                            colorHex = [22, 163, 74]; // Verde (Green 600) - Por si lo necesitas a futuro
                        }

                        // Dibujar círculo estético
                        doc.setFillColor(...colorHex);
                        doc.circle(18, y - 1.5, 2, 'F'); // x, y, radio, style

                        // Título de la acción
                        doc.setTextColor(15, 23, 42); // Texto muy oscuro
                        doc.setFontSize(11);
                        doc.setFont("helvetica", "bold");
                        doc.text(item.titulo, 23, y);
                        
                        y += 6;
                        
                        // Valor detectado con círculo pequeño para status
                        doc.setFontSize(9);
                        doc.setFont("helvetica", "normal");
                        doc.setTextColor(100, 116, 139); // Gris pizarra medio
                        doc.text(`Valor actual detectado: ${item.valorActual}  |  Prioridad: ${item.prioridad}`, 23, y);
                        
                        y += 7;
                        
                        // Acción recomendada (Bloque de texto)
                        doc.setTextColor(51, 65, 85); // Gris oscuro para lectura
                        const lineasAccion = doc.splitTextToSize(`Acción: ${item.accion}`, 173); // Ajustado por el margen del círculo
                        doc.text(lineasAccion, 23, y);
                        
                        y += (lineasAccion.length * 5) + 10; // Espaciado extra para respirar entre items
                    });
                    
                    y += 5; // Espacio extra antes de la siguiente dimensión
                });
            }
            
            // Pie de página con fecha de generación
            const totalPages = doc.internal.getNumberOfPages();
            const dateStr = new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
            
            for (let i = 1; i <= totalPages; i++) {
                doc.setPage(i);
                doc.setFontSize(8);
                doc.setTextColor(148, 163, 184); // Gris muy claro
                doc.text(`Generado por DiME Team el ${dateStr} - Página ${i} de ${totalPages}`, 105, 290, { align: "center" });
            }

            doc.save("Plan_de_Accion_DiME.pdf");

        } catch (error) {
            console.error("❌ Error en la ejecución:", error);
            alert("Hubo un error al generar el plan de acción. Revisa tu conexión o sesión.");
        } finally {
            btnGenerar.innerText = "📥 Descargar Plan de Acción en PDF";
            btnGenerar.style.pointerEvents = "auto";
        }
    });
});
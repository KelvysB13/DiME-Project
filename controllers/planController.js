// --- 1. DICCIONARIOS ---
const diccionarioAcciones = {
    "tasa_reclamos_ROJO": "Auditar la causa raíz de los reclamos más recientes (producto, despacho, comunicación) y congelar o pausar las publicaciones con reclamos recurrentes mientras se corrige el origen.",
    "tasa_reclamos_AMARILLO": "Revisar las últimas 20 órdenes con reclamo para identificar un patrón común antes de que el indicador escale.",
    "tasa_cancelaciones_ROJO": "Auditar de inmediato el flujo de sincronización de stock y pricing automático; identificar si el origen es falta de stock, error de precio o falla logística.",
    "tasa_cancelaciones_AMARILLO": "Identificar el origen específico de las cancelaciones recientes y corregirlo antes de eventos de alto volumen.",
    "tasa_mediaciones_ROJO": "Capacitar al equipo de atención en resolución proactiva de reclamos y revisar si hay reclamos abiertos sin respuesta que estén escalando por defecto.",
    "tasa_envios_incorrectos_ROJO": "Auditar de inmediato el proceso de despacho (picking/packing); es la causa raíz más probable detrás del deterioro de reclamos y mediaciones.",
    "nivel_reputacion_ROJO": "Priorizar la corrección del KPI base con peor desviación como primer paso del plan de recuperación de 60 días.",
    "insignia_ROJO": "Corregir primero reclamos y mediaciones (causa más probable de la pérdida de insignia) antes de evaluar cualquier otra palanca comercial.",
    "cvr_global_ROJO": "Revisar en conjunto fotos, ficha técnica, precio competitivo y estado del termómetro de reputación antes de invertir más presupuesto en tráfico pago.",
    "cvr_global_AMARILLO": "Diagnosticar si el cuello de botella está en precio, fotos o reputación antes de escalar inversión en tráfico.",
    "margen_neto_real_ROJO": "Desglosar de inmediato comisiones, envío, ads y descuento por reputación para identificar la fuga principal de margen.",
    "carga_total_costos_ROJO": "Desglosar cada componente de costo y atacar primero el de mayor peso individual sobre las ventas brutas.",
    "tasa_cobro_efectivo_ROJO": "Revisar el estado de los reclamos activos como primera hipótesis antes de explorar otras causas de la brecha de cobro.",
    "crecimiento_mom_ROJO": "Revisar en conjunto reputación, conversión y eficiencia de publicidad, dado que una caída de ingresos rara vez tiene una sola causa aislada.",
    "puntaje_calidad_ROJO": "Revisar título, atributos y multimedia de las publicaciones con peor puntaje, priorizando las de mayor potencial de tráfico.",
    "cvr_publicacion_ROJO": "Auditar la publicación (precio, fotos, ficha) o darla de baja si tras la corrección no mejora.",
    "pct_catalogo_completo_ROJO": "Completar las características técnicas faltantes priorizando los SKUs de mayor tráfico.",
    "pct_publicaciones_con_video_ROJO": "Priorizar la incorporación de video en las publicaciones de mayor tráfico.",
    "roas_ROJO": "Pausar o reestructurar de inmediato las campañas con este nivel de retorno antes de seguir comprometiendo presupuesto.",
    "inversion_ads_sobre_ventas_ROJO": "Evaluar si el tráfico orgánico puede asumir parte de la carga actual sostenida por ads.",
    "dead_stock_rate_ROJO": "Auditar de inmediato el catálogo para definir qué SKUs liquidar, promocionar o retirar de Full.",
    "antiguedad_riesgo_ROJO": "Aplicar liquidación, descuento agresivo o retiro de bodega sobre los SKUs específicos que ya están generando cargos.",
    "overstock_rate_ROJO": "Recalcular las proyecciones de reposición antes del próximo envío a Full para alinear stock con demanda real.",
    "utilizacion_espacios_ROJO": "Si es baja, evaluar ampliar el catálogo; si es alta, liberar espacio para reducir riesgo de quiebre en productos estrella.",
    "tiene_banner_ROJO": "Instalar banner profesional como acción prioritaria; es uno de los cambios de menor costo y mayor impacto.",
    "tiene_carruseles_ROJO": "Activar los carrousels de productos junto con la organización de categorías para mejorar navegación.",
    "categorias_organizadas_ROJO": "Reorganizar categorías priorizando las líneas de producto de mayor tráfico."
};

const planesIntegrados = [
    {
        nombre: "Colapso de Conversión y Costos",
        prioridad: "Urgente",
        condiciones: [ ["cvr_global_ROJO"], ["carga_total_costos_ROJO"], ["margen_neto_real_ROJO"] ],
        accion: "1) Pausar cualquier escalamiento de tráfico o ads. 2) Resolver primero conversión (fotos, ficha, precio) y estructura de costos. 3) Solo después de estabilizar ambos frentes, evaluar inversión de crecimiento."
    },
    {
        nombre: "Acumulación Crítica de Cargos Full",
        prioridad: "Urgente",
        condiciones: [ ["dead_stock_rate_ROJO"], ["antiguedad_riesgo_ROJO"] ],
        accion: "1) Priorizar liquidación por antigüedad: los SKUs más viejos primero, para frenar cargos diarios. 2) Una vez controlados, atacar el resto del dead stock."
    }
];

// --- 2. TRADUCTOR DE NOMBRES ---
// Convierte lo que manda el backend ("Tasa de Conversión Global (CVR)") a nuestra llave ("cvr_global")
function obtenerLlaveBase(nombreKpi) {
    const n = nombreKpi.toLowerCase();
    if (n.includes("reclamos")) return "tasa_reclamos";
    if (n.includes("cancelaciones")) return "tasa_cancelaciones";
    if (n.includes("mediaciones")) return "tasa_mediaciones";
    if (n.includes("incorrectos")) return "tasa_envios_incorrectos";
    if (n.includes("reputación") || n.includes("termómetro")) return "nivel_reputacion";
    if (n.includes("insignia")) return "insignia";
    if (n.includes("conversión") || n.includes("cvr")) return "cvr_global";
    if (n.includes("margen")) return "margen_neto_real";
    if (n.includes("ticket") || n.includes("aov")) return "ticket_promedio";
    if (n.includes("carga") || n.includes("costos")) return "carga_total_costos";
    if (n.includes("intención")) return "ratio_intencion_compra";
    if (n.includes("descuento")) return "descuento_reputacion";
    if (n.includes("cobro")) return "tasa_cobro_efectivo";
    if (n.includes("crecimiento")) return "crecimiento_mom";
    if (n.includes("puntaje") || n.includes("calidad")) return "puntaje_calidad";
    if (n.includes("cobertura") || n.includes("fotos")) return "cobertura_fotos";
    if (n.includes("catálogo") || n.includes("características")) return "pct_catalogo_completo";
    if (n.includes("video")) return "pct_publicaciones_con_video";
    if (n.includes("roas")) return "roas";
    if (n.includes("acos")) return "acos";
    if (n.includes("inversión")) return "inversion_ads_sobre_ventas";
    if (n.includes("dead stock") || n.includes("rotación")) return "dead_stock_rate";
    if (n.includes("antigüedad") || n.includes("riesgo")) return "antiguedad_riesgo";
    if (n.includes("aptos")) return "productos_no_aptos";
    if (n.includes("overstock") || n.includes("exceso")) return "overstock_rate";
    if (n.includes("espacios") || n.includes("utilización")) return "utilizacion_espacios";
    if (n.includes("banner")) return "tiene_banner";
    if (n.includes("logo")) return "tiene_logo";
    if (n.includes("carrusel") || n.includes("carrousel")) return "tiene_carruseles";
    if (n.includes("categorías")) return "categorias_organizadas";
    
    return "desconocido";
}

// --- 3. LÓGICA PRINCIPAL ---
document.addEventListener('DOMContentLoaded', () => {
    const btnGenerar = document.getElementById('btn-generate-plan');
    
    if (!btnGenerar) return;

    btnGenerar.addEventListener('click', async () => {
        try {
            // Cambio visual de carga
            btnGenerar.innerText = "⏳ Auditando métricas y generando PDF...";
            btnGenerar.style.pointerEvents = "none";
            
            const token = localStorage.getItem('access_token');
            const vendedorId = localStorage.getItem('vendedor_id') || 1; // Valor por defecto parar probar
    
            
            if (!vendedorId) {
                alert("Error: Sesión de vendedor no encontrada.");
                return;
            }

            const headers = {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''
            };

            // Petición al backend
            const response = await fetch(`/api/kpis-query?vendedor_id=${vendedorId}`, { headers });
            if (!response.ok) throw new Error("Fallo en la comunicación con el servidor.");
            
            const dataKpis = await response.json();
            
            // Creamos las firmas traducidas
            const firmasActuales = new Set();
            dataKpis.items.forEach(kpi => {
                const llaveBase = obtenerLlaveBase(kpi.nombre_kpi);
                firmasActuales.add(`${llaveBase}_${kpi.estado_semaforo.toUpperCase()}`);
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
                        valorActual: "Múltiples métricas afectadas"
                    });
                    
                    plan.condiciones.forEach(grupo => {
                        grupo.forEach(c => kpisProcesadosEnCombinacion.add(c));
                    });
                }
            });

            // Evaluar KPIs Individuales
            dataKpis.items.forEach(kpi => {
                const llaveBase = obtenerLlaveBase(kpi.nombre_kpi);
                const firma = `${llaveBase}_${kpi.estado_semaforo.toUpperCase()}`;
                
                if ((kpi.estado_semaforo === 'ROJO' || kpi.estado_semaforo === 'AMARILLO') && !kpisProcesadosEnCombinacion.has(firma)) {
                    
                    // Aquí la magia: Si el traductor no lo encuentra, usa un mensaje por defecto, pero si lo encuentra, lanza la acción
                    const accionRecomendada = diccionarioAcciones[firma] || `Requiere atención en el módulo de ${kpi.dimension}.`;
                    
                    planFinal.push({
                        titulo: `${kpi.nombre_kpi} (${kpi.dimension})`,
                        prioridad: kpi.prioridad || "Atención", 
                        accion: accionRecomendada,
                        valorActual: kpi.valor_actual || "N/A"
                    });
                }
            });

            // Ordenar urgentes primero
            planFinal.sort((a, b) => {
                const priorA = (a.prioridad || "").toUpperCase();
                const priorB = (b.prioridad || "").toUpperCase();
                if (priorA.includes("URGENTE") && !priorB.includes("URGENTE")) return -1;
                if (!priorA.includes("URGENTE") && priorB.includes("URGENTE")) return 1;
                return 0;
            });

            // --- GENERACIÓN DEL PDF ---
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            // Encabezado
            doc.setFillColor(15, 23, 42); // Azul oscuro DiME
            doc.rect(0, 0, 210, 30, 'F');
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(20);
            doc.setFont("helvetica", "bold");
            doc.text("Plan de Accion Estrategico - DiME", 15, 20);
            
            let y = 45;
            
            if (planFinal.length === 0) {
                doc.setTextColor(21, 128, 61); // Verde
                doc.setFontSize(14);
                doc.text("¡Felicidades! Todos tus indicadores están en niveles óptimos.", 15, y);
            } else {
                planFinal.forEach((item, index) => {
                    // Control de salto de página
                    if (y > 260) {
                        doc.addPage();
                        y = 20;
                    }
                    
                    // Título y Prioridad
                    doc.setFontSize(12);
                    doc.setFont("helvetica", "bold");
                    
                    if ((item.prioridad || "").toUpperCase().includes('URGENTE') || item.titulo.includes('CRÍTICO')) {
                        doc.setTextColor(220, 38, 38); // Rojo
                    } else {
                        doc.setTextColor(202, 138, 4); // Amarillo/Naranja
                    }
                    
                    doc.text(`${index + 1}. ${item.titulo}`, 15, y);
                    y += 6;
                    
                    // Valor detectado
                    doc.setFontSize(10);
                    doc.setFont("helvetica", "normal");
                    doc.setTextColor(100, 100, 100);
                    doc.text(`Valor detectado: ${item.valorActual}`, 15, y);
                    y += 6;
                    
                    // Acción recomendada (con salto de línea automático)
                    doc.setTextColor(40, 40, 40);
                    const lineasAccion = doc.splitTextToSize(`Accion: ${item.accion}`, 180);
                    doc.text(lineasAccion, 15, y);
                    
                    y += (lineasAccion.length * 5) + 10; // Espaciado para el siguiente ítem
                });
            }
            
            // Descargar archivo
            doc.save("Plan_de_Accion_DiME.pdf");

        } catch (error) {
            console.error("❌ Error en la ejecución:", error);
            alert("Hubo un error al generar el plan de acción. Revisa tu conexión o sesión.");
        } finally {
            // Restaurar botón
            btnGenerar.innerText = "📥 Descargar Plan de Acción";
            btnGenerar.style.pointerEvents = "auto";
        }
    });
});
// Plantillas de texto DIAGNÓSTICO (analítico, sin recomendaciones de acción) por KPI
// y estado de semáforo — fuente: "Reglas de Negocio — Diagnóstico Automatizado de KPIs".
// Esto es DISTINTO del diccionario de acciones de kpiActionsService.js (usado por el
// PDF del Plan de Acción, que no se toca acá). Depende de obtenerLlaveBase() y
// normalizarSemaforo(), definidas en kpiActionsService.js — debe cargarse después.

const diccionarioDiagnostico = {

    // --- 1. REPUTACIÓN & CALIDAD DE SERVICIO ---
    "tasa_reclamos_VERDE": "Tu tasa de reclamos de {valor}% mantiene el termómetro en verde y la elegibilidad a Platinum vigente. Este nivel refleja que la combinación de calidad de producto, comunicación y cumplimiento del compromiso de entrega está funcionando dentro de los parámetros que ML exige para no penalizar la visibilidad orgánica.",
    "tasa_reclamos_AMARILLO": "Con {valor}% de reclamos, la cuenta está en zona de riesgo dentro de la ventana de evaluación de 60 días. Este rango todavía no activa la caída del termómetro, pero cualquier pico adicional —típico en eventos de alto volumen como CyberDay— puede empujarla al umbral crítico antes de que cierre el ciclo de evaluación.",
    "tasa_reclamos_ROJO": "El {valor}% de reclamos ya deterioró el termómetro a rojo, lo que se traduce en una caída de ventas estimada de 20–40% solo por pérdida de visibilidad orgánica, y no únicamente en las publicaciones que originaron los reclamos sino en la totalidad del catálogo. Dado que ML reevalúa en ventanas de 60 días, el impacto comercial se extiende considerablemente más allá del problema puntual que lo originó.",

    "tasa_cancelaciones_VERDE": "Con {valor}% de cancelaciones por vendedor, la operación demuestra control sobre stock, precios y capacidad logística. ML pondera estas cancelaciones de forma más severa que las del comprador, por lo que este nivel es indicativo de procesos internos sólidos.",
    "tasa_cancelaciones_AMARILLO": "El {valor}% de cancelaciones comunica al algoritmo una señal de pérdida parcial de control operativo, incluso si el origen es puntual. En este rango el riesgo principal es que coincida con otros KPIs de reputación deteriorados y acelere la caída del termómetro.",
    "tasa_cancelaciones_ROJO": "El {valor}% de cancelaciones es una señal crítica de pérdida de control operativo. ML las penaliza con mayor severidad que las del comprador porque comunican una falla de gestión directa —inventario, pricing o capacidad logística— y este patrón suele coexistir con deterioro simultáneo en otros KPIs de reputación.",

    "tasa_mediaciones_VERDE": "Con {valor}% de mediaciones, los conflictos se resuelven en la conversación directa con el comprador antes de requerir intervención de ML. Esto pesa más positivamente en el termómetro que una baja tasa de reclamos simple, porque demuestra capacidad de resolución autónoma.",
    "tasa_mediaciones_AMARILLO": "El {valor}% de mediaciones indica que una porción de los reclamos no se está resolviendo en conversación directa, lo que empuja la intervención de ML. Es un síntoma más grave que un reclamo aislado, porque refleja una falla en el proceso de resolución, no solo en el producto o servicio original.",
    "tasa_mediaciones_ROJO": "El {valor}% de mediaciones indica incapacidad sistemática de resolver conflictos directamente con el comprador, lo que tiene mayor peso negativo en el termómetro que los reclamos básicos. Este patrón generalmente coexiste con una tasa de reclamos también elevada, ya que las mediaciones son, en su mayoría, consecuencia de reclamos no resueltos.",

    "tasa_envios_incorrectos_VERDE": "Con {valor}% de envíos incorrectos, el proceso de picking/packing es confiable. Dado que el consumidor chileno tiene mayor exigencia de post-venta que el promedio LATAM, mantener este control reduce directamente la exposición a reclamos y mediaciones aguas abajo.",
    "tasa_envios_incorrectos_AMARILLO": "El {valor}% de envíos incorrectos está cerca del umbral crítico. Cada envío erróneo es un generador directo de reclamos y mediaciones, por lo que este KPI suele anticipar deterioro en esos dos indicadores antes de que se manifieste en el termómetro general.",
    "tasa_envios_incorrectos_ROJO": "El {valor}% de envíos incorrectos es crítico y, dado el mayor nivel de exigencia del consumidor chileno frente al resto de LATAM, amplifica el impacto negativo en reclamos y mediaciones de forma desproporcionada. Este KPI suele ser la causa raíz logística detrás de un termómetro deteriorado, más que un síntoma aislado.",

    "nivel_reputacion_VERDE": "El termómetro en {valor} (verde) implica ausencia de restricciones de visibilidad y acceso pleno a beneficios. Es el resultado consolidado de mantener reclamos, cancelaciones y mediaciones simultáneamente bajo control.",
    "nivel_reputacion_AMARILLO": "El termómetro en {valor} es zona de actuación: el deterioro ya es visible para el algoritmo, aunque aún no alcanzó el punto de máxima penalización. El KPI base específico que esté empujando este nivel (reclamos, cancelaciones, mediaciones o envíos incorrectos) determina la severidad real detrás de esta cifra.",
    "nivel_reputacion_ROJO": "El termómetro en {valor} (rojo) implica una caída esperada de ventas del 20–40% por pérdida de visibilidad orgánica en la totalidad del catálogo, no solo en las publicaciones problemáticas. La recuperación toma hasta 60 días desde que se corrigen las causas subyacentes, lo que hace de este KPI el de mayor impacto comercial acumulado de toda la dimensión de reputación.",

    "insignia_VERDE": "La insignia {valor} (Platinum) convierte entre 10–25% más que no tener insignia, según datos de agencias LATAM. Sostener este nivel requiere reclamos < 1% y cancelaciones < 2% de forma continua en los últimos 60 días de evaluación.",
    "insignia_AMARILLO": "La insignia {valor} (Silver) indica que la cuenta cumple parcialmente los requisitos de calidad, pero no ambos simultáneamente (reclamos < 1% y cancelaciones < 2%). Es una posición intermedia que depende de cuál de los dos KPIs base está limitando el ascenso.",
    "insignia_ROJO": "No tener insignia ({valor}) es una desventaja competitiva directa frente a vendedores Platinum o Silver en el mismo resultado de búsqueda, incluyendo menor conversión relativa por falta de la señal de confianza que aporta el badge. Esta condición suele ser consecuencia directa de un termómetro deteriorado, no un problema aislado de insignia.",

    // --- 2. VENTAS & RENTABILIDAD ---
    "cvr_global_VERDE": "El CVR de {valor}% es sólido: fotos, descripción, precio competitivo y reputación están funcionando en conjunto como un funnel saludable. Este número resume en un solo dato la salud comercial integral de la cuenta.",
    "cvr_global_AMARILLO": "Con {valor}% de CVR, el funnel convierte por debajo de su potencial. Este rango no permite distinguir por sí solo si el cuello de botella está en precio, multimedia o reputación; requiere lectura cruzada con esos KPIs para aislar la causa.",
    "cvr_global_ROJO": "El CVR de {valor}% es crítico: el problema no es de volumen de tráfico sino de conversión de ese tráfico. Una CVR baja sostenida en presencia de visitas normales o altas es la señal más clara de que fotos, ficha técnica, precio o reputación están fallando simultáneamente.",

    "margen_neto_real_VERDE": "Tu Payout Rate es de {valor}%, lo que significa que Mercado Libre te transfiere más del 70% de cada venta. Esto indica que tu estructura de comisiones y cargos por envío es eficiente. Estás en el rango superior de los vendedores de MercadoLibre, donde el take-rate promedio de la plataforma suele estar entre el 20% y el 30% (dejando un 70-80% de liquidación).",
    "margen_neto_real_AMARILLO": "Tu Payout Rate es de {valor}%, lo que significa que Mercado Libre está reteniendo entre el 30% y el 40% de tus ventas en comisiones y cargos. Este nivel es común en cuentas que ofrecen muchas cuotas sin interés, tienen costos de envío elevados, o pagan comisiones por categorías de alto take-rate. Aunque no es crítico, reduce tu capacidad de maniobra para absorber otros costos operativos.",
    "margen_neto_real_ROJO": "Tu Payout Rate es de solo {valor}%, lo que significa que Mercado Libre se está llevando más del 40% de tus ventas. Esto es extremadamente alto y te deja casi sin margen para cubrir el costo del producto y otros gastos. Las causas más probables son: (1) Termómetro de reputación en rojo que activa descuentos adicionales, (2) Categoría con comisiones altas (>20%), (3) Oferta excesiva de cuotas sin interés, o (4) Costos de envío desproporcionados para tu ticket promedio. En cualquiera de estos casos, cada venta que haces te acerca más a la pérdida operativa.",

    "ticket_promedio_VERDE": "El AOV de USD {valor} está por sobre el benchmark de mercados con ads activos (mediana ~USD 74, Triple Whale 2025), lo que otorga margen de maniobra para invertir en calidad de publicación y envío sin destruir rentabilidad.",
    "ticket_promedio_AMARILLO": "Con un AOV de USD {valor}, la operación depende de volumen consistente para que ads y envío no erosionen el margen, ya que el ticket por sí solo no absorbe holgadamente esos costos fijos por transacción.",
    "ticket_promedio_ROJO": "Un AOV de USD {valor} combinado con publicidad activa hace el margen prácticamente imposible: el costo de adquisición por venta tiende a superar lo que la transacción puede sostener, generando pérdida estructural en cada conversión proveniente de ads.",

    "ratio_intencion_compra_VERDE": "El ratio de intención de {valor}% muestra tráfico de calidad: una proporción alta de visitantes realiza una acción de compra (carrito, preguntas), lo que indica que el problema de funnel, si existe, está más cerca del cierre que de la atracción.",
    "ratio_intencion_compra_AMARILLO": "Con {valor}% de intención de compra, existe interés genuino pero algo frena el cierre. Esta combinación —intención media sin conversión proporcional— suele apuntar a fricción de precio o desconfianza derivada del estado de reputación, más que a un problema de tráfico.",
    "ratio_intencion_compra_ROJO": "El {valor}% de intención de compra es crítico: indica un problema de calidad de tráfico o de la publicación misma, no solo de conversión final. Una intención baja sugiere que el tráfico que llega no corresponde al perfil de comprador del producto, o que la publicación no logra generar interés real más allá de la visita.",

    "descuento_reputacion_VERDE": "No existe penalización por reputación ({valor}%), lo que confirma que el termómetro está saludable y que el margen no tiene fugas ocultas por este concepto.",
    "descuento_reputacion_AMARILLO": "La cuenta está perdiendo {valor}% de sus ventas brutas en comisiones extra por reputación. Es un costo silencioso que no aparece en el estado de resultados como una línea explícita, pero que reduce el margen neto de forma sistemática mientras el termómetro no mejore.",
    "descuento_reputacion_ROJO": "El {valor}% perdido en descuento por reputación es una penalización significativa y, a diferencia de otros costos operativos, es enteramente atribuible al estado del termómetro, no a la estructura de precios o logística. Esta cifra suele representar una fuga de margen mayor de lo que la cuenta percibe.",

    "tasa_cobro_efectivo_VERDE": "La tasa de cobro efectivo de {valor}% está cercana al 100% esperado, lo que indica que el ciclo de liquidación opera sin fricciones significativas.",
    "tasa_cobro_efectivo_AMARILLO": "El {valor}% de cobro efectivo refleja una brecha relevante entre lo facturado y lo realmente cobrado, probablemente explicada por ventas pendientes de liberación o retenciones asociadas a reclamos abiertos.",
    "tasa_cobro_efectivo_ROJO": "Solo se está cobrando {valor}% de las ventas brutas. Esta brecha casi siempre se explica por reclamos abiertos que retienen el pago, lo que conecta directamente este KPI con el estado de la dimensión de reputación más que con un problema puramente financiero.",

    "crecimiento_mom_VERDE": "Un crecimiento de {valor}% MoM supera el ritmo del mercado chileno (~9.9% anual, CCS 2025), lo que indica ganancia de participación relativa y no solo acompañamiento del crecimiento sectorial.",
    "crecimiento_mom_AMARILLO": "Un crecimiento de {valor}% MoM está en línea con el ritmo del mercado, pero sin ganar cuota de forma diferenciada. Sostenido en el tiempo, este nivel equivale a mantener posición relativa sin destacar frente a la competencia.",
    "crecimiento_mom_ROJO": "Un {valor}% (decrecimiento) implica pérdida activa de participación de mercado en un sector que crece ~9.9% anual. Esta caída rara vez tiene una sola causa: típicamente coincide con deterioro simultáneo en conversión, reputación o eficiencia de publicidad.",

    // --- 3. CALIDAD & RENDIMIENTO DE PUBLICACIONES ---
    "puntaje_calidad_VERDE": "Un puntaje de {valor} otorga prioridad máxima en el buscador de ML. Es la variable de mayor retorno por esfuerzo de toda la dimensión de catálogo, porque su efecto se multiplica sobre cada publicación que la alcanza.",
    "puntaje_calidad_AMARILLO": "Un puntaje de {valor} deja la publicación en zona media de visibilidad: ni penalizada ni priorizada. El componente específico que falta (fotos, características, descripción) determina cuánto está costando este nivel intermedio en exposición orgánica.",
    "puntaje_calidad_ROJO": "Un puntaje de {valor} implica ausencia de visibilidad orgánica relevante. Por encima de cualquier otra fortaleza de la cuenta —precio competitivo, buena reputación—, el algoritmo simplemente no está mostrando estas publicaciones con suficiente frecuencia.",

    "cvr_publicacion_VERDE": "Esta publicación convierte {valor}% de sus visitas, por sobre el benchmark de calidad para el funnel a nivel de ítem.",
    "cvr_publicacion_AMARILLO": "Con {valor}% de conversión, la publicación funciona pero sin destacar. En este rango el funnel no está roto, pero tampoco está optimizado frente a su potencial de tráfico.",
    "cvr_publicacion_ROJO": "Esta publicación convierte solo {valor}% tras un volumen relevante de visitas, lo que indica que está drenando tráfico sin generar ventas proporcionales, con efecto negativo sobre el score general de la cuenta.",

    "cobertura_fotos_VERDE": "Con {valor} fotos y video, la publicación está en el estándar óptimo. Las publicaciones con 8+ fotos muestran hasta 60% más CVR que las de 1–2, por lo que este nivel de inversión visual se traduce de forma directa en conversión.",
    "cobertura_fotos_AMARILLO": "Con {valor} fotos, la publicación está por debajo del mínimo recomendado de 5, lo que la deja en un punto medio de efectividad visual frente al benchmark documentado.",
    "cobertura_fotos_ROJO": "Con solo {valor} fotos, el CVR de esta publicación está siendo penalizado de forma directa: el diferencial documentado entre 1–2 fotos y 8+ fotos es de hasta 60% de conversión, lo que convierte este déficit en uno de los de mayor impacto cuantificable del catálogo.",

    "pct_catalogo_completo_VERDE": "Con {valor}% del catálogo con ficha técnica completa, la cuenta captura al segmento de 40–60% de compradores que filtran por especificaciones técnicas, en lugar de perderlos antes de la visita.",
    "pct_catalogo_completo_AMARILLO": "El {valor}% del catálogo con ficha completa deja una porción relevante de publicaciones potencialmente invisibles para compradores que buscan por filtros específicos.",
    "pct_catalogo_completo_ROJO": "Solo {valor}% del catálogo tiene ficha técnica completa, lo que hace a la mayoría del inventario invisible para el 40–60% de compradores que filtran por especificaciones. Este KPI afecta el volumen de tráfico calificado que llega a la publicación, no solo su conversión posterior.",

    "pct_publicaciones_con_video_VERDE": "Con {valor}% del catálogo activo con video, la cuenta está usando el diferenciador de contenido más sub-utilizado en MLC, lo que se traduce en CVR consistentemente más alta frente a la competencia que no lo usa.",
    "pct_publicaciones_con_video_AMARILLO": "El {valor}% de cobertura de video deja a la mayoría del catálogo sin este diferenciador, cuyo impacto en conversión es mayor precisamente en los SKUs de más tráfico.",
    "pct_publicaciones_con_video_ROJO": "Con solo {valor}% de video en el catálogo, la cuenta está dejando sin capturar un diferencial de conversión documentado y de bajo costo de implementación relativo a su impacto.",

    // --- 4. PUBLICIDAD — PRODUCT ADS ---
    "roas_VERDE": "Un ROAS de {valor}x es sólido para un objetivo de campaña enfocado en rentabilidad: cada peso invertido en ads retorna varias veces su valor en ventas generadas.",
    "roas_AMARILLO": "Un ROAS de {valor}x corresponde a una fase de crecimiento o defensa de categoría, no de pura rentabilidad. Es un nivel aceptable solo si el objetivo declarado de la campaña es volumen, y se acerca al umbral donde deja de serlo.",
    "roas_ROJO": "Un ROAS de {valor}x significa pérdida real: cada peso invertido en ads no se recupera en ventas generadas. Esta condición convierte la inversión publicitaria en un drenaje neto de margen, independiente de cuál sea el objetivo declarado de la campaña.",

    "acos_VERDE": "Un ACoS de {valor}% está alineado con un objetivo de rentabilidad: el margen actual de la cuenta sostiene este nivel de inversión publicitaria sin destruir valor.",
    "acos_AMARILLO": "Un ACoS de {valor}% corresponde a una estrategia de crecimiento de volumen. Su sostenibilidad depende enteramente del margen bruto real de la cuenta; el mismo número puede ser saludable o insostenible según ese contexto.",
    "acos_ROJO": "Un ACoS de {valor}% es inviable en cualquier contexto de margen razonable. La regla de referencia (ACoS sostenible ≤ (margen bruto − costos fijos) × 60%) confirma que, salvo márgenes excepcionalmente altos, este nivel destruye rentabilidad en cada venta proveniente de ads.",

    "inversion_ads_sobre_ventas_VERDE": "La dependencia de ads es baja ({valor}%): la tracción de la cuenta es mayormente orgánica, y la publicidad cumple un rol de aceleración más que de sostén de ventas.",
    "inversion_ads_sobre_ventas_AMARILLO": "Con {valor}% de las ventas dependiendo de inversión publicitaria, la cuenta se acerca al umbral de dependencia estructural, donde el tráfico orgánico ya no es suficiente para sostener el volumen actual de ventas.",
    "inversion_ads_sobre_ventas_ROJO": "Se requiere invertir {valor}% de las ventas brutas en ads solo para mantener el nivel actual de ventas. Esto constituye dependencia crítica: sin un componente orgánico saludable detrás (reputación, calidad de publicación), el crecimiento de la cuenta no es sostenible en el tiempo.",

    "participacion_estrategica_ofertas_VERDE": "La participación en eventos clave con análisis de margen previo ({valor}) permite capturar los picos de 3–10x venta diaria que reportan los vendedores estratégicos en CyberDay, sin comprometer rentabilidad.",
    "participacion_estrategica_ofertas_AMARILLO": "La participación en ofertas ({valor}) sin evaluación previa de margen puede estar generando volumen a costa de rentabilidad sin que la cuenta lo perciba directamente en el resultado del evento.",
    "participacion_estrategica_ofertas_ROJO": "La ausencia de participación en eventos clave como CyberDay ({valor}) representa una oportunidad de ingreso significativa no capturada, considerando que vendedores estratégicos reportan picos de 3–10x venta diaria normal en estas fechas.",

    "descuento_promedio_ofrecido_VERDE": "Un descuento promedio de {valor}% está en el rango donde el consumidor chileno activa la compra sin que se perciba una pérdida de margen significativa frente al volumen generado.",
    "descuento_promedio_ofrecido_AMARILLO": "Con {valor}% de descuento promedio, la tracción generada probablemente es limitada: en Chile el consumidor responde de forma más marcada en el rango 15–30%, por lo que este nivel deja valor sin capturar en términos de activación de demanda.",
    "descuento_promedio_ofrecido_ROJO": "Un descuento promedio de {valor}% supera el umbral donde el consumidor chileno empieza a desconfiar de la calidad del producto, además de destruir margen de forma directa. El efecto combinado (menor margen + percepción de menor calidad) es mayor que la suma de ambos problemas por separado.",

    "cupones_aplicados_VERDE": "El crecimiento MoM sostenido en cupones aplicados ({valor}) indica que la audiencia de 'Mi Página' está activa y respondiendo a la estrategia de fidelización dentro del ecosistema ML.",
    "cupones_aplicados_AMARILLO": "Un nivel estable de cupones aplicados ({valor}) no muestra caída, pero tampoco crecimiento, lo que sugiere que la base de seguidores ya conocida no se está expandiendo ni reactivando con nuevas ofertas.",
    "cupones_aplicados_ROJO": "El decrecimiento o ausencia de cupones aplicados ({valor}) es señal de que la audiencia de seguidores no está activada. Desde el cierre de Mercado Shops en diciembre de 2025, este KPI es uno de los indicadores más directos de fidelización dentro del ecosistema ML.",

    // --- 5. STOCK FULL — EFICIENCIA DE INVENTARIO ---
    "dead_stock_rate_VERDE": "Con {valor}% de dead stock, el inventario en Full está prácticamente libre de capital congelado.",
    "dead_stock_rate_AMARILLO": "El {valor}% de inventario sin movimiento representa capital empezando a inmovilizarse, en un rango donde aún no se activan cargos relevantes por antigüedad, pero la tendencia ya es observable.",
    "dead_stock_rate_ROJO": "El {valor}% de dead stock representa simultáneamente dinero congelado y cargos de almacenamiento crecientes, lo que lo convierte en un drenaje silencioso de margen operativo que no se refleja en el estado de ventas brutas.",

    "antiguedad_riesgo_VERDE": "Con {valor}% de productos en zona de antigüedad de riesgo, no hay exposición relevante a cargos por almacenamiento prolongado.",
    "antiguedad_riesgo_AMARILLO": "El {valor}% de SKUs entrando en zona de antigüedad de riesgo (> 2 meses en Full) indica un volumen de inventario que, sin intervención, comenzará a generar cargos diarios crecientes en el corto plazo.",
    "antiguedad_riesgo_ROJO": "El {valor}% de SKUs ya está generando cargos por antigüedad que afectan el margen de forma directa y medible, distinto del riesgo latente del tramo amarillo.",

    "productos_no_aptos_VERDE": "La ausencia de productos marcados como no aptos ({valor}%) indica que el proceso de empaque y envío a bodega está funcionando sin fricciones de calidad.",
    "productos_no_aptos_AMARILLO": "Un nivel bajo de productos no aptos ({valor}%) es vigilable: la relevancia diagnóstica está en si se concentra en un proveedor o transportista específico, o si está distribuido de forma aleatoria en el catálogo.",
    "productos_no_aptos_ROJO": "El {valor}% de unidades en Full marcadas como no aptas genera pérdidas directas: ocupan espacio, generan cargos y no producen ingresos. Es uno de los pocos KPIs de esta dimensión donde el umbral ideal es estrictamente cero, no un rango.",

    "overstock_rate_VERDE": "El nivel de sobrestock ({valor}%) está ajustado a la demanda proyectada, dentro del rango de 30–60 días de cobertura considerado saludable.",
    "overstock_rate_AMARILLO": "El {valor}% del catálogo con más unidades en Full de las que la demanda puede absorber indica una desalineación moderada entre reposición y demanda real, antes de que se traduzca en cargos por antigüedad.",
    "overstock_rate_ROJO": "Con {valor}% de sobrestock, la planificación de reposición no está alineada con la demanda real, lo que anticipa cargos por antigüedad en el corto plazo si el patrón se mantiene.",

    "utilizacion_espacios_VERDE": "La utilización de {valor}% está en la zona óptima: la capacidad asignada se usa de forma productiva, con flexibilidad suficiente para absorber variaciones de reposición.",
    "utilizacion_espacios_AMARILLO": "Con {valor}% de utilización, existe espacio asignado que no se está usando de forma productiva, lo que representa capacidad pagada pero subaprovechada.",
    "utilizacion_espacios_ROJO": "Una utilización de {valor}% es un extremo problemático: si es baja, refleja capacidad ociosa; si es muy alta, indica riesgo concreto de quiebre de stock en productos estrella por falta de margen operativo de espacio.",

    // --- 6. MI PÁGINA & PRESENCIA DE TIENDA ---
    "tiene_banner_VERDE": "El banner de tienda está {valor} (presente), lo que refuerza la confianza profesional percibida por el comprador y, con ello, contribuye positivamente al CVR.",
    "tiene_banner_AMARILLO": "El banner está {valor}, pero desalineado con la oferta o campaña vigente. Una imagen desactualizada reduce parcialmente su efecto de confianza frente a uno alineado con la propuesta comercial actual.",
    "tiene_banner_ROJO": "La ausencia de banner ({valor}) deja a la tienda sin uno de los elementos visuales que más directamente comunican profesionalismo en la primera impresión del comprador.",

    "tiene_logo_VERDE": "El logo está {valor} (presente), aportando identidad de marca y diferenciación frente a otros vendedores de la misma categoría.",
    "tiene_logo_AMARILLO": "El logo está {valor}, pero inconsistente con la identidad visual usada en otros canales de la marca, lo que diluye parcialmente el reconocimiento.",
    "tiene_logo_ROJO": "La ausencia de logo de marca ({valor}) deja a la tienda compitiendo únicamente por precio y reputación, sin un elemento de diferenciación visual propio.",

    "tiene_carruseles_VERDE": "Los carrousels están {valor} (activos), favoreciendo el descubrimiento de catálogo y, con ello, el AOV potencial de cada visita a 'Mi Página'.",
    "tiene_carruseles_AMARILLO": "Los carrousels están {valor}, configurados solo en parte del catálogo, lo que limita el descubrimiento a un subconjunto de la oferta disponible.",
    "tiene_carruseles_ROJO": "Los carrousels están {valor} (inactivos), lo que limita el descubrimiento de catálogo de los seguidores que visitan 'Mi Página' y reduce el AOV potencial de esas visitas.",

    "categorias_organizadas_VERDE": "Las categorías están {valor} (organizadas), lo que mejora la experiencia de navegación y la conversión de los seguidores dentro de 'Mi Página'.",
    "categorias_organizadas_AMARILLO": "Las categorías están {valor}, parcialmente estructuradas, lo que genera una experiencia de navegación inconsistente entre distintas líneas de producto.",
    "categorias_organizadas_ROJO": "Las categorías están {valor} (desorganizadas), lo que dificulta la navegación del seguidor y reduce la probabilidad de descubrimiento y conversión dentro de la tienda."
};

function formatearValorDiagnostico(valor) {
    if (valor === null || valor === undefined || valor === '') return 'N/A';
    if (typeof valor === 'number') {
        return Number.isInteger(valor) ? String(valor) : valor.toFixed(2);
    }
    return String(valor);
}

// Arma los mensajes diagnósticos (analíticos) a partir de los items de /api/kpis-query,
// uno por KPI — sin combinaciones ni deduplicación (eso es exclusivo del Plan de Acción).
function obtenerMensajesDiagnostico(kpiItems) {
    const mensajes = [];

    kpiItems.forEach(kpi => {
        const llaveBase = obtenerLlaveBase(kpi.nombre_kpi);

        if (llaveBase === "carga_total_costos" || llaveBase === "desconocido") {
            return;
        }

        const semaforoReal = normalizarSemaforo(kpi.estado_semaforo);
        if (semaforoReal !== 'ROJO' && semaforoReal !== 'AMARILLO' && semaforoReal !== 'VERDE') {
            return;
        }

        const firma = `${llaveBase}_${semaforoReal}`;
        const plantilla = diccionarioDiagnostico[firma];
        if (!plantilla) return;

        let tituloMostrar = kpi.nombre_kpi;
        if (llaveBase === "margen_neto_real") {
            tituloMostrar = "Payout Rate";
        }

        mensajes.push({
            titulo: tituloMostrar,
            texto: plantilla.replace(/\{valor\}/g, formatearValorDiagnostico(kpi.valor_actual)),
            dimension: kpi.dimension || "Otros",
            semaforo: semaforoReal
        });
    });

    return mensajes;
}

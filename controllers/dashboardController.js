const apiBase = '/api';

const DIAG_SECTIONS = ['reputacion', 'ventas', 'calidad', 'inventario', 'publicidad'];
const PLAN_MAP = { 1: 'Gratuito', 2: 'Pro', 3: 'Enterprise' };
const REPUTATION_COLORS = {
  green: { color: '#10B981', label: 'Excelente' },
  yellow: { color: '#F59E0B', label: 'En observación' },
  red: { color: '#EF4444', label: 'Crítico' }
};
let state = {
  selectedSellerId: null,
  sellers: {},
  publications: [],
  filteredPublications: [],
  currentUser: null,
  usingMockData: false
};

function getToken() {
  return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
}

function getRefreshToken() {
  return localStorage.getItem('refresh_token') || sessionStorage.getItem('refresh_token');
}

function decodeJwtPayload(token) {
  try {
    const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const json = decodeURIComponent(atob(base64).split('').map(c =>
      '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));
    return JSON.parse(json);
  } catch {
    return null;
  }
}

function getVendedorId() {
  const token = getToken();
  if (!token) return null;
  const payload = decodeJwtPayload(token);
  return payload ? payload.sub : null;
}

async function loadDiagnosticoEmbeds() {
  const vendedorId = getVendedorId();

  if (!vendedorId) {
    DIAG_SECTIONS.forEach((key) => {
      const emptyEl = document.getElementById(`diag-${key}-empty`);
      const embedEl = document.getElementById(`diag-${key}-embed`);
      if (!emptyEl || !embedEl) return;
      emptyEl.textContent = 'Inicia sesión para ver este diagnóstico.';
      emptyEl.style.display = 'block';
      embedEl.style.display = 'none';
    });
    return;
  }

  let embedUrls = {};
  try {
    // El backend genera URLs firmadas con el id_vendedor de la sesión ya "bloqueado" —
    // el visitante no puede verlo ni cambiarlo desde el navegador.
    embedUrls = await apiFetch('/metabase/embed-urls');
  } catch {
    embedUrls = {};
  }

  DIAG_SECTIONS.forEach((key) => {
    const emptyEl = document.getElementById(`diag-${key}-empty`);
    const embedEl = document.getElementById(`diag-${key}-embed`);
    const iframe = document.getElementById(`diag-${key}-iframe`);
    const loadingEl = document.getElementById(`diag-${key}-loading`);
    const dashboardUrl = embedUrls[key];

    if (!emptyEl || !embedEl || !iframe) return;

    if (!dashboardUrl) {
      emptyEl.textContent = 'No se pudo cargar este diagnóstico. Intenta de nuevo más tarde.';
      emptyEl.style.display = 'block';
      embedEl.style.display = 'none';
      return;
    }

    iframe.src = dashboardUrl;
    emptyEl.style.display = 'none';
    embedEl.style.display = 'block';

    if (loadingEl) loadingEl.classList.remove('diag-loading-hidden');
    iframe.addEventListener('load', function onLoad() {
      if (loadingEl) loadingEl.classList.add('diag-loading-hidden');
      iframe.removeEventListener('load', onLoad);
    }, { once: true });
  });
}

// Traduce la "dimension" que manda /api/kpis-query (misma que usa el PDF del Plan
// de Acción) a la sección del panel de Diagnóstico donde debe mostrarse el mensaje.
const DIMENSION_TO_SECTION = {
  'Reputación': 'reputacion',
  'Finanzas': 'ventas',
  'Publicaciones': 'calidad',
  'Logística': 'inventario',
  'Publicidad': 'publicidad'
};

async function loadDiagnosticoInsights() {
  const vendedorId = getVendedorId();
  if (!vendedorId) return;

  DIAG_SECTIONS.forEach((key) => {
    const container = document.getElementById(`diag-${key}-insights`);
    if (container) container.innerHTML = '';
  });

  let items = [];
  try {
    const data = await apiFetch(`/kpis-query?vendedor_id=${vendedorId}`);
    // Mensajes analíticos (sin acciones) para la barra de Diagnóstico — distintos
    // de calcularPlanFinal(), que es exclusivo del PDF del Plan de Acción.
    items = obtenerMensajesDiagnostico(data.items || []);
  } catch {
    return;
  }

  items.forEach((item) => {
    const sectionKey = DIMENSION_TO_SECTION[item.dimension];
    const container = sectionKey && document.getElementById(`diag-${sectionKey}-insights`);
    if (!container) return;
    container.appendChild(crearAccordionItem(item.titulo, item.texto, item.semaforo));
  });
}

// Tarjeta de acordeón reutilizada por Diagnóstico y por la lista del Plan de Acción:
// muestra solo el título, y al hacer clic despliega el texto completo debajo.
function crearAccordionItem(titulo, texto, semaforo) {
  const div = document.createElement('div');
  div.className = `diag-insight-item semaforo-${semaforo}`;
  div.innerHTML = `
    <button type="button" class="diag-insight-toggle">
      <span class="diag-insight-title"></span>
      <svg class="diag-insight-caret" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <p class="diag-insight-text"></p>
  `;
  div.querySelector('.diag-insight-title').textContent = titulo;
  div.querySelector('.diag-insight-text').textContent = texto;
  div.querySelector('.diag-insight-toggle').addEventListener('click', () => {
    div.classList.toggle('open');
  });
  return div;
}

async function loadPlanAccionList() {
  const container = document.getElementById('action-plan-list');
  if (!container) return;

  const vendedorId = getVendedorId();
  if (!vendedorId) return;

  let planFinal = [];
  try {
    const data = await apiFetch(`/kpis-query?vendedor_id=${vendedorId}`);
    // Misma fuente que usa el PDF (planController.js) — así la lista en pantalla
    // y el PDF descargado siempre muestran exactamente lo mismo.
    planFinal = calcularPlanFinal(data.items || []);
  } catch {
    return;
  }

  container.innerHTML = '';

  if (planFinal.length === 0) {
    const p = document.createElement('p');
    p.style.cssText = 'font-size:13px;color:var(--text-secondary);margin-top:16px;';
    p.textContent = '¡Felicidades! Todos tus indicadores están en niveles óptimos.';
    container.appendChild(p);
    return;
  }

  const agrupados = planFinal.reduce((acc, item) => {
    if (!acc[item.dimension]) acc[item.dimension] = [];
    acc[item.dimension].push(item);
    return acc;
  }, {});

  Object.keys(agrupados).forEach((dimension) => {
    const heading = document.createElement('h4');
    heading.className = 'plan-dimension-heading';
    heading.textContent = dimension;
    container.appendChild(heading);

    agrupados[dimension].forEach((item) => {
      container.appendChild(crearAccordionItem(item.titulo, item.accion, item.semaforo));
    });
  });
}

async function apiFetch(url, options = {}) {
  const token = getToken();
  const headers = { ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const response = await fetch(apiBase + url, { ...options, headers });
  if (response.status === 401) {
    const refreshed = await tryRefresh();
    if (refreshed) {
      const newToken = getToken();
      headers['Authorization'] = `Bearer ${newToken}`;
      return fetch(apiBase + url, { ...options, headers });
    }
    redirectToLogin();
  }
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Error en la solicitud' }));
    throw new Error(err.detail || 'Error en la solicitud');
  }
  return response.json();
}

async function tryRefresh() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;
  try {
    const resp = await fetch(apiBase + '/auth/refresh', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken })
    });
    if (!resp.ok) return false;
    const d = await resp.json();
    const storage = localStorage.getItem('access_token') ? localStorage : sessionStorage;
    storage.setItem('access_token', d.access_token);
    storage.setItem('refresh_token', d.refresh_token);
    return true;
  } catch { return false; }
}

function redirectToLogin() {
  ['access_token','refresh_token','user_id','user_name'].forEach(k => localStorage.removeItem(k));
  sessionStorage.clear();
  window.location.href = '/auth/login';
}

function formatCurrency(val, d) {
  d = d || 2;
  if (val == null || isNaN(val)) return '-';
  return parseFloat(val).toLocaleString('es', { minimumFractionDigits: d, maximumFractionDigits: d });
}
function formatNumber(val) {
  if (val == null || isNaN(val)) return '-';
  return parseInt(val).toLocaleString('es');
}
function formatBool(v) { return v == null ? '-' : v ? 'Sí' : 'No'; }

function badgeClass(nivel) {
  return { green: 'badge-green', yellow: 'badge-yellow', red: 'badge-red' }[nivel] || '';
}
function statusClass(est) {
  return { active: 'status-active', paused: 'status-paused', closed: 'status-closed', under_review: 'status-under-review' }[est] || 'status-active';
}

const MOCK_SELLERS = {
  1: {
    id: 1, user_name: 'Tecno Hogar AR', nombre_tienda: 'TecnoHogar S.A.',
    email: 'ventas@tecnohogar.com.ar', codigo_pais: 'AR', moneda_local: 'ARS', tipo_plan: 2,
    reputacion: { nivel_reputacion: 'green', insignia: 'MercadoLíder Platino', total_reclamos: 12, total_canceladas: 5, total_mediaciones: 3, total_envios_incorrectos: 8 },
    negocio: { ventas_brutas_moneda_local: 2847500.50, ventas_brutas_usd: 2850.00, unidades_vendidas: 342, visitas_totales: 28500, ventas_concretadas: 342, precio_promedio_venta: 8326.00 },
    costos: { ventas_cobradas_total: 2562750.45, neto_recibido: 2178337.88, cargos_por_venta: 384412.57, costos_envio: 125000.00, inversion_ads: 45000.00, descuento_reputacion: 0 },
    stock_full: { puntaje_calidad: 87, espacios_p_asignados: 45, espacios_g_asignados: 12, productos_no_aptos_venta: 3, productos_sin_rotacion: 8, productos_antiguedad: 5 },
    mi_pagina: { tiene_banner: true, tiene_logo: true, tiene_carruseles: true, categories_organizadas: true },
    alertas: [
      { nivel: 'high', mensaje: '3 productos sin rotación > 90 días' },
      { nivel: 'medium', mensaje: 'Tasa de reclamos aumentó 15% este mes' },
      { nivel: 'low', mensaje: 'Stock bajo en 2 espacios G' }
    ],
    categorias: [
      { nombre: 'Electrónica', ventas: 45, margen: 32, color: 'accent' },
      { nombre: 'Celulares', ventas: 28, margen: 28, color: 'primary' },
      { nombre: 'Accesorios', ventas: 18, margen: 45, color: 'purple' },
      { nombre: 'Audio', ventas: 9, margen: 22, color: 'rose' }
    ],
    publicaciones: [
      { titulo: 'Auriculares Bluetooth Pro', ml_item_id: 'MLA-1234567890', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 2840, ventas: 125, calidad: 92 },
      { titulo: 'Cargador Rápido USB-C 65W', ml_item_id: 'MLA-1234567891', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 1520, ventas: 89, calidad: 88 },
      { titulo: 'Funda Silicona iPhone 15', ml_item_id: 'MLA-1234567892', tipo_publicacion: 'bronze', estado_publicacion: 'active', visitas: 3200, ventas: 210, calidad: 75 },
      { titulo: 'Smartwatch Deportivo X200', ml_item_id: 'MLA-1234567893', tipo_publicacion: 'gold_premium', estado_publicacion: 'active', visitas: 980, ventas: 42, calidad: 95 },
      { titulo: 'Parlante Portátil Resistente', ml_item_id: 'MLA-1234567894', tipo_publicacion: 'bronze', estado_publicacion: 'paused', visitas: 450, ventas: 18, calidad: 70 },
      { titulo: 'Hub USB-C 7 en 1', ml_item_id: 'MLA-1234567895', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 1850, ventas: 95, calidad: 85 }
    ],
    metabaseCharts: [
      { title: 'Panel de Ventas', url: 'http://localhost:3000/public/question/3aa4fffb-05e9-4635-bf0f-3bf2d8c32b18' },
      { title: 'Reputación', url: 'http://localhost:3000/embed/dashboard/2' },
      { title: 'Costos', url: 'http://localhost:3000/embed/dashboard/3' },
      { title: 'Stock Full', url: 'http://localhost:3000/embed/dashboard/4' },
      { title: 'Tráfico', url: 'http://localhost:3000/embed/dashboard/5' }
    ]
  },
  2: {
    id: 2, user_name: 'Moda Infantil VE', nombre_tienda: 'Moda Infantil Caracas C.A.',
    email: 'contacto@modainfantil.com', codigo_pais: 'VE', moneda_local: 'USD', tipo_plan: 1,
    reputacion: { nivel_reputacion: 'yellow', insignia: 'MercadoLíder', total_reclamos: 28, total_canceladas: 12, total_mediaciones: 7, total_envios_incorrectos: 15 },
    negocio: { ventas_brutas_moneda_local: 12500.00, ventas_brutas_usd: 12500.00, unidades_vendidas: 180, visitas_totales: 12400, ventas_concretadas: 180, precio_promedio_venta: 69.44 },
    costos: { ventas_cobradas_total: 11250.00, neto_recibido: 9562.50, cargos_por_venta: 1687.50, costos_envio: 3200.00, inversion_ads: 12000.00, descuento_reputacion: 250.00 },
    stock_full: { puntaje_calidad: 68, espacios_p_asignados: 22, espacios_g_asignados: 8, productos_no_aptos_venta: 7, productos_sin_rotacion: 14, productos_antiguedad: 9 },
    mi_pagina: { tiene_banner: true, tiene_logo: true, tiene_carruseles: false, categories_organizadas: true },
    alertas: [
      { nivel: 'high', mensaje: 'Puntaje de calidad por debajo del mínimo (68/100)' },
      { nivel: 'high', mensaje: '14 productos sin rotación en inventario' },
      { nivel: 'medium', mensaje: 'Descuento por reputación activo: -$250 USD' }
    ],
    categorias: [
      { nombre: 'Ropa Bebés', ventas: 52, margen: 38, color: 'accent' },
      { nombre: 'Juguetes', ventas: 30, margen: 25, color: 'primary' },
      { nombre: 'Calzado', ventas: 12, margen: 42, color: 'purple' },
      { nombre: 'Accesorios', ventas: 6, margen: 35, color: 'rose' }
    ],
    publicaciones: [
      { titulo: 'Set de Ropa Bebé 6 Piezas', ml_item_id: 'MLV-9876543210', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 1890, ventas: 78, calidad: 72 },
      { titulo: 'Juguete Educativo Bloques 100pz', ml_item_id: 'MLV-9876543211', tipo_publicacion: 'bronze', estado_publicacion: 'active', visitas: 2450, ventas: 112, calidad: 65 },
      { titulo: 'Zapatos Escolares Talla 28', ml_item_id: 'MLV-9876543212', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 780, ventas: 34, calidad: 80 },
      { titulo: 'Cuna Plegable Viajera', ml_item_id: 'MLV-9876543213', tipo_publicacion: 'gold_premium', estado_publicacion: 'paused', visitas: 320, ventas: 8, calidad: 90 },
      { titulo: 'Mochila Infantil Dinosaurio', ml_item_id: 'MLV-9876543214', tipo_publicacion: 'bronze', estado_publicacion: 'active', visitas: 1100, ventas: 55, calidad: 60 }
    ],
    metabaseCharts: [
      { title: 'Panel de Ventas', url: 'http://localhost:3000/embed/dashboard/6' },
      { title: 'Reputación', url: 'http://localhost:3000/embed/dashboard/7' },
      { title: 'Costos', url: 'http://localhost:3000/embed/dashboard/8' }
    ]
  },
  3: {
    id: 3, user_name: 'Tecno Chile', nombre_tienda: 'Tecno Chile SpA',
    email: 'ventas@tecnochile.cl', codigo_pais: 'CL', moneda_local: 'CLP', tipo_plan: 2,
    reputacion: { nivel_reputacion: 'green', insignia: 'MercadoLíder Platino', total_reclamos: 5, total_canceladas: 2, total_mediaciones: 1, total_envios_incorrectos: 3 },
    negocio: { ventas_brutas_moneda_local: 18750000, ventas_brutas_usd: 20500.00, unidades_vendidas: 520, visitas_totales: 42000, ventas_concretadas: 520, precio_promedio_venta: 36057.69 },
    costos: { ventas_cobradas_total: 16875000, neto_recibido: 14343750, cargos_por_venta: 2531250, costos_envio: 890000, inversion_ads: 350000, descuento_reputacion: 0 },
    stock_full: { puntaje_calidad: 94, espacios_p_asignados: 68, espacios_g_asignados: 20, productos_no_aptos_venta: 1, productos_sin_rotacion: 3, productos_antiguedad: 2 },
    mi_pagina: { tiene_banner: true, tiene_logo: true, tiene_carruseles: true, categories_organizadas: true },
    alertas: [
      { nivel: 'low', mensaje: '3 espacios P con ocupación > 85%' },
      { nivel: 'low', mensaje: 'Actualizar fotos de 2 publicaciones antiguas' }
    ],
    categorias: [
      { nombre: 'Computación', ventas: 42, margen: 35, color: 'accent' },
      { nombre: 'Periféricos', ventas: 30, margen: 40, color: 'primary' },
      { nombre: 'Almacenamiento', ventas: 18, margen: 30, color: 'purple' },
      { nombre: 'Redes', ventas: 10, margen: 38, color: 'rose' }
    ],
    publicaciones: [
      { titulo: 'Notebook Gamer RTX 4060', ml_item_id: 'MLC-5551112220', tipo_publicacion: 'gold_premium', estado_publicacion: 'active', visitas: 4200, ventas: 85, calidad: 98 },
      { titulo: 'Monitor 27" 4K IPS', ml_item_id: 'MLC-5551112221', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 3500, ventas: 120, calidad: 95 },
      { titulo: 'Teclado Mecánico RGB', ml_item_id: 'MLC-5551112222', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 5600, ventas: 230, calidad: 88 },
      { titulo: 'SSD NVMe 1TB', ml_item_id: 'MLC-5551112223', tipo_publicacion: 'bronze', estado_publicacion: 'active', visitas: 2800, ventas: 145, calidad: 82 },
      { titulo: 'Mouse Inalámbrico Pro', ml_item_id: 'MLC-5551112224', tipo_publicacion: 'gold_special', estado_publicacion: 'active', visitas: 3100, ventas: 178, calidad: 90 },
      { titulo: 'Webcam 4K Streaming', ml_item_id: 'MLC-5551112225', tipo_publicacion: 'bronze', estado_publicacion: 'active', visitas: 1200, ventas: 52, calidad: 75 },
      { titulo: 'Hub Thunderbolt 4', ml_item_id: 'MLC-5551112226', tipo_publicacion: 'gold_premium', estado_publicacion: 'paused', visitas: 680, ventas: 22, calidad: 93 }
    ],
    metabaseCharts: [
      { title: 'Panel de Ventas', url: 'http://localhost:3000/embed/dashboard/9' },
      { title: 'Reputación', url: 'http://localhost:3000/embed/dashboard/10' },
      { title: 'Costos', url: 'http://localhost:3000/embed/dashboard/11' },
      { title: 'Stock Full', url: 'http://localhost:3000/embed/dashboard/12' },
      { title: 'Tráfico', url: 'http://localhost:3000/embed/dashboard/13' },
      { title: 'Publicaciones', url: 'http://localhost:3000/embed/dashboard/14' },
      { title: 'Mi Página', url: 'http://localhost:3000/embed/dashboard/15' }
    ]
  }
};

function renderSellerRibbon(seller) {
  const el = document.getElementById('seller-ribbon');
  if (!seller) { el.innerHTML = '<span style="color:var(--text-muted);font-size:12px">Selecciona un vendedor</span>'; return; }
  el.innerHTML = `
    <span class="seller-ribbon-label">Tienda</span>
    <span class="seller-ribbon-value">${seller.nombre_tienda}</span>
    <div class="seller-ribbon-divider"></div>
    <span class="seller-ribbon-label">País</span>
    <span class="seller-ribbon-value">${seller.codigo_pais}</span>
    <div class="seller-ribbon-divider"></div>
    <span class="seller-ribbon-label">Moneda</span>
    <span class="seller-ribbon-value">${seller.moneda_local}</span>
    <div class="seller-ribbon-divider"></div>
    <span class="seller-ribbon-label">Plan</span>
    <span class="seller-ribbon-value">${PLAN_MAP[seller.tipo_plan] || 'Gratuito'}</span>
    <div class="seller-ribbon-divider"></div>
    <span class="seller-ribbon-label">Insignia</span>
    <span class="seller-ribbon-value"><span class="badge ${badgeClass(seller.reputacion.nivel_reputacion)}">${seller.reputacion.insignia || 'Sin insignia'}</span></span>
  `;
}

function renderKpiCards(seller) {
  const grid = document.getElementById('kpi-cards');
  if (!seller) { grid.innerHTML = ''; return; }
  const r = seller.reputacion, n = seller.negocio, c = seller.costos, s = seller.stock_full, p = seller.mi_pagina;
  const cards = [
    { label: 'Reputación', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>', colorClass: 'icon-yellow', barColor: '#FCD703', value: r.insignia || 'Sin datos', trend: formatNumber(r.total_reclamos) + ' reclamos', trendClass: r.total_reclamos > 15 ? 'warning' : 'positive', detail: 'Canceladas: ' + formatNumber(r.total_canceladas) + ' · Mediaciones: ' + formatNumber(r.total_mediaciones) },
    { label: 'Negocio', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>', colorClass: 'icon-green', barColor: '#12AA78', value: formatCurrency(n.ventas_brutas_moneda_local), trend: formatNumber(n.unidades_vendidas) + ' uds vendidas', trendClass: 'positive', detail: formatNumber(n.visitas_totales) + ' visitas · ' + formatNumber(n.ventas_concretadas) + ' ventas' },
    { label: 'Costos', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>', colorClass: 'icon-red', barColor: '#EF4444', value: formatCurrency(c.neto_recibido), trend: 'Comisiones: ' + formatCurrency(c.cargos_por_venta), trendClass: 'neutral', detail: 'Envíos: ' + formatCurrency(c.costos_envio) + ' · Ads: ' + formatCurrency(c.inversion_ads) },
    { label: 'Stock Full', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>', colorClass: 'icon-orange', barColor: '#DB730F', value: s.puntaje_calidad + '/100', trend: formatNumber(s.espacios_p_asignados) + ' espacios P', trendClass: s.puntaje_calidad >= 80 ? 'positive' : 'warning', detail: formatNumber(s.productos_no_aptos_venta) + ' no aptos · ' + formatNumber(s.productos_sin_rotacion) + ' sin rotación' },
    { label: 'Mi Página', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>', colorClass: 'icon-yellow', barColor: '#FCD703', value: formatBool(p.tiene_banner), trend: formatBool(p.tiene_logo), trendClass: 'positive', detail: 'Carruseles: ' + formatBool(p.tiene_carruseles) + ' · Cats: ' + formatBool(p.categories_organizadas) },
    { label: 'Cuenta', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>', colorClass: 'icon-green', barColor: '#12AA78', value: seller.user_name || '-', trend: seller.email || '-', trendClass: 'neutral', detail: seller.codigo_pais + ' · ' + (PLAN_MAP[seller.tipo_plan] || 'Gratuito') }
  ];
  grid.innerHTML = cards.map(k => `
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-label">${k.label}</span>
        <div class="kpi-icon-box ${k.colorClass}">${k.icon}</div>
      </div>
      <div class="kpi-value">${k.value}</div>
      <div class="kpi-trend ${k.trendClass}">${k.trend}</div>
      <div class="kpi-mini-chart">
        ${Array.from({length:12}, (_,i) => '<div class="bar" style="height:' + (Math.floor(Math.random()*16)+6) + 'px;background:' + k.barColor + '"></div>').join('')}
      </div>
      <div style="font-size:10px;color:var(--text-secondary);font-family:'JetBrains Mono',monospace;margin-top:6px">${k.detail}</div>
    </div>
  `).join('');
}

function renderReputationDial(seller) {
  const container = document.getElementById('dial-container');
  const titleEl = document.getElementById('rep-badge-title');
  const detailsEl = document.getElementById('dial-details');
  if (!seller) { container.innerHTML = ''; titleEl.textContent = '-'; detailsEl.innerHTML = ''; return; }
  const r = seller.reputacion;
  const totalIssues = r.total_reclamos + r.total_canceladas + r.total_mediaciones + r.total_envios_incorrectos;
  let score = Math.max(0, Math.min(100, 100 - totalIssues * 2));
  const lc = REPUTATION_COLORS[r.nivel_reputacion] || REPUTATION_COLORS.yellow;
  titleEl.textContent = r.insignia || 'Sin insignia';
  titleEl.style.color = lc.color;
  const circ = 2 * Math.PI * 36;
  const offset = circ * (1 - score / 100);
  container.innerHTML = `
    <svg width="100" height="90" viewBox="0 0 100 90">
      <path d="M 12 78 A 36 36 0 1 1 88 78" fill="none" stroke="var(--border-light)" stroke-width="6" stroke-linecap="round"/>
      <path d="M 12 78 A 36 36 0 1 1 88 78" fill="none" stroke="${lc.color}" stroke-width="6" stroke-linecap="round" stroke-dasharray="${circ}" stroke-dashoffset="${offset}" style="transition:stroke-dashoffset 1s ease-out"/>
    </svg>
    <div class="dial-score">
      <div class="dial-score-value" style="color:${lc.color}">${score}</div>
      <div class="dial-score-label">Puntaje</div>
    </div>`;
  const maxV = Math.max(r.total_reclamos, r.total_canceladas, r.total_mediaciones, r.total_envios_incorrectos, 1);
  const items = [
    { label: 'Reclamos', value: r.total_reclamos },
    { label: 'Cancelaciones', value: r.total_canceladas },
    { label: 'Mediaciones', value: r.total_mediaciones },
    { label: 'Envíos Incorrectos', value: r.total_envios_incorrectos }
  ];
  detailsEl.innerHTML = items.map(item => `
    <div class="detail-row">
      <span class="detail-label">${item.label}</span>
      <div class="detail-bar-wrap">
        <div class="detail-bar-bg"><div class="detail-bar-fill" style="width:${(item.value/maxV)*100}%;background:${lc.color}"></div></div>
        <span class="detail-value">${item.value}</span>
      </div>
    </div>
  `).join('');
}

function renderAlerts(seller) {
  const el = document.getElementById('alerts-container');
  if (!seller || !seller.alertas || !seller.alertas.length) { el.innerHTML = '<span style="font-size:11px;color:var(--text-muted)">Sin alertas activas ✓</span>'; return; }
  el.innerHTML = seller.alertas.map(a => `<div class="alert-card alert-${a.nivel}"><span>${a.nivel==='high'?'🔴':a.nivel==='medium'?'🟡':'🟢'}</span><span>${a.mensaje}</span></div>`).join('');
}

function renderCategoryPerformance(seller) {
  const el = document.getElementById('category-performance');
  if (!seller || !seller.categorias || !seller.categorias.length) { el.innerHTML = '<span style="font-size:11px;color:var(--text-muted)">Sin datos</span>'; return; }
  const maxV = Math.max(...seller.categorias.map(c => c.ventas));
  el.innerHTML = seller.categorias.map(c => `
    <div>
      <div class="flex items-center justify-between" style="font-size:10px;margin-bottom:4px">
        <span style="color:var(--text-secondary)">${c.nombre}</span>
        <span class="font-mono font-semibold" style="color:var(--text)">${c.ventas}% · ${c.margen}% margen</span>
      </div>
      <div class="cat-bar"><div class="cat-bar-fill cat-bar-${c.color}" style="width:${(c.ventas/maxV)*100}%"></div></div>
    </div>
  `).join('');
}

function renderPublicationsTable(seller) {
  const tbody = document.getElementById('publications-tbody');
  const catFilter = document.getElementById('pub-category-filter');
  if (!seller || !seller.publicaciones || !seller.publicaciones.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:24px;font-size:12px">Sin publicaciones disponibles</td></tr>';
    return;
  }
  state.publications = seller.publicaciones;
  state.filteredPublications = [...seller.publicaciones];
  const tipos = [...new Set(seller.publicaciones.map(p => p.tipo_publicacion))];
  catFilter.innerHTML = '<option value="Todas">Todas las categorías</option>' + tipos.map(t => `<option value="${t}">${t.replace(/_/g,' ').toUpperCase()}</option>`).join('');
  applyFilters();
}

function applyFilters() {
  const term = document.getElementById('pub-search').value.toLowerCase();
  const cat = document.getElementById('pub-category-filter').value;
  state.filteredPublications = state.publications.filter(p => {
    const ms = !term || p.titulo.toLowerCase().includes(term) || p.ml_item_id.toLowerCase().includes(term);
    const mc = cat === 'Todas' || p.tipo_publicacion === cat;
    return ms && mc;
  });
  renderFilteredPublications();
}

function renderFilteredPublications() {
  const tbody = document.getElementById('publications-tbody');
  if (!state.filteredPublications.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:24px;font-size:12px">Sin resultados</td></tr>'; return;
  }
  tbody.innerHTML = state.filteredPublications.map(p => `
    <tr>
      <td class="font-semibold" style="color:var(--primary)">${p.titulo}</td>
      <td><code style="color:var(--warning);font-size:11px">${p.ml_item_id}</code></td>
      <td style="color:var(--text-secondary)">${p.tipo_publicacion.replace(/_/g,' ').toUpperCase()}</td>
      <td style="text-align:center"><span class="status-badge ${statusClass(p.estado_publicacion)}">${p.estado_publicacion}</span></td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace">${formatNumber(p.visitas)}</td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace">${formatNumber(p.ventas)}</td>
      <td style="text-align:center;font-family:'JetBrains Mono',monospace">${p.calidad}/100</td>
    </tr>
  `).join('');
}

function adaptDashboardData(apiData) {
  const reputacion = apiData.reputacion || {};
  const negocio = apiData.negocio || {};
  const costos = apiData.costos || {};
  const stock = apiData.stock || {};
  const pagina = apiData.pagina || {};
  
  return {
    id: apiData.tipo_plan || 1,
    user_name: apiData.nombre_tienda || 'Vendedor',
    nombre_tienda: apiData.nombre_tienda || 'Mi Tienda',
    email: '',
    codigo_pais: apiData.codigo_pais || 'AR',
    moneda_local: apiData.codigo_pais === 'VE' ? 'USD' : (apiData.codigo_pais === 'AR' ? 'ARS' : 'USD'),
    tipo_plan: apiData.tipo_plan || 1,
    reputacion: {
      nivel_reputacion: reputacion.nivel || 'yellow',
      insignia: reputacion.insignia || 'Sin insignia',
      total_reclamos: reputacion.total_reclamos || 0,
      total_canceladas: reputacion.total_canceladas || 0,
      total_mediaciones: reputacion.total_mediaciones || 0,
      total_envios_incorrectos: 0,
      tasa_reclamos: reputacion.tasa_reclamos || 0.0
    },
    negocio: {
      ventas_brutas_moneda_local: negocio.ventas_brutas_moneda_local || 0.0,
      unidades_vendidas: negocio.unidades_vendidas || 0,
      visitas_totales: negocio.visitas_totales || 0,
      ventas_concretadas: negocio.ventas_concretadas || 0
    },
    costos: {
      ventas_cobradas_total: costos.ventas_cobradas_total || 0.0,
      neto_recibido: costos.neto_recibido || 0.0,
      cargos_por_venta: costos.cargos_por_venta || 0.0,
      costos_envio: costos.costos_envio || 0.0,
      inversion_ads: costos.inversion_ads || 0.0,
      descuento_reputacion: 0
    },
    stock_full: {
      puntaje_calidad: stock.puntaje_calidad || 0,
      espacios_p_asignados: stock.espacios_p_asignados || 0,
      espacios_g_asignados: 0,
      productos_no_aptos_venta: stock.productos_no_aptos_venta || 0,
      productos_sin_rotacion: stock.productos_sin_rotacion || 0,
      productos_antiguedad: 0
    },
    mi_pagina: {
      tiene_banner: pagina.tiene_banner || false,
      tiene_logo: pagina.tiene_logo || false,
      tiene_carruseles: pagina.tiene_carruseles || false,
      categories_organizadas: pagina.categorias_organizadas || false
    },
    alertas: [
      ...(stock.productos_sin_rotacion > 0 ? [{ nivel: 'high', mensaje: `${stock.productos_sin_rotacion} productos sin rotación` }] : []),
      ...(stock.puntaje_calidad < 80 ? [{ nivel: 'medium', mensaje: 'Puntaje de calidad bajo' }] : [])
    ],
    categorias: [
      { nombre: 'General', ventas: 100, margen: 0, color: 'primary' }
    ],
    publicaciones: (apiData.publicaciones || []).map(p => ({
      titulo: p.titulo,
      ml_item_id: p.ml_item_id,
      tipo_publicacion: p.tipo_publicacion,
      estado_publicacion: p.estado_publicacion,
      visitas: p.visitas,
      ventas: p.ventas,
      calidad: p.puntaje_calidad || 0
    })),
    metabaseCharts: []
  };
}

function renderMetabaseFilter() {
  const container = document.getElementById('metabase-filter');
  container.innerHTML = '';
  Object.values(state.sellers).forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'metabase-filter-btn' + (state.selectedSellerId === s.id ? ' active' : '');
    btn.textContent = s.user_name + ' (' + s.metabaseCharts.length + ')';
    btn.dataset.id = s.id;
    btn.addEventListener('click', () => {
      state.selectedSellerId = s.id;
      renderMetabaseFilter();
      renderMetabaseCharts();
    });
    container.appendChild(btn);
  });
}

function renderMetabaseCharts() {
  const container = document.getElementById('metabase-charts');
  const countEl = document.getElementById('metabase-chart-count');
  const seller = state.sellers[state.selectedSellerId];
  const metabaseSection = document.getElementById('metabaseSection');
  if (!seller || !seller.metabaseCharts || !seller.metabaseCharts.length) {
    if (metabaseSection) metabaseSection.style.display = 'none';
    container.innerHTML = '<p class="metabase-empty">No hay gráficos de Metabase configurados para este vendedor.</p>';
    countEl.textContent = '0 gráficos'; return;
  }
  if (metabaseSection) metabaseSection.style.display = 'block';
  countEl.textContent = seller.metabaseCharts.length + ' gráficos';
  container.innerHTML = seller.metabaseCharts.map(ch => `
    <div class="metabase-chart-card">
      <div class="metabase-chart-title">${ch.title}</div>
      <iframe src="${ch.url}#bordered=true&titled=true" loading="lazy" allowtransparency></iframe>
    </div>
  `).join('');
}

function updateDashboard(sellerId) {
  state.selectedSellerId = sellerId;
  const seller = state.sellers[sellerId];
  if (seller) {
    const welcomeNameNode = document.getElementById('welcome-store-name');
    if (welcomeNameNode) {
      welcomeNameNode.textContent = seller.nombre_tienda || seller.user_name;
    }

    document.getElementById('profile-name').textContent = seller.user_name;
    document.getElementById('profile-plan').textContent = PLAN_MAP[seller.tipo_plan] || 'Gratuito';
    document.getElementById('dropdown-name').textContent = seller.nombre_tienda;
    document.getElementById('dropdown-email').textContent = seller.email;
    document.getElementById('profile-avatar-letter').textContent = seller.user_name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase() || 'DM';

    document.getElementById('topbar-title').textContent = 'Dashboard: ' + seller.user_name;
  }

  renderSellerRibbon(seller);
  renderKpiCards(seller);
  renderAlerts(seller);
  renderCategoryPerformance(seller);
  renderPublicationsTable(seller);
  renderMetabaseFilter();
  renderMetabaseCharts();
  document.getElementById('update-timestamp').textContent = 'Actualizado: ' + new Date().toLocaleString('es');
  document.getElementById('data-source-label').textContent = state.usingMockData ? ' • Mock Data' : '';
  document.getElementById('loadingSpinner').style.display = 'none';
  document.getElementById('dashboardContent').style.display = 'block';
}

async function loadDashboard() {
  try {
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('dashboardContent').style.display = 'none';
    
    // general-information y dashboard son independientes entre sí — se piden en
    // paralelo para no sumar sus tiempos de espera uno detrás del otro.
    const [userInfoResult, dashDataResult] = await Promise.allSettled([
      apiFetch('/general-information'),
      apiFetch('/dashboard')
    ]);

    let userInfo = null;
    if (userInfoResult.status === 'fulfilled') {
      userInfo = userInfoResult.value;
      state.currentUser = userInfo;
    } else {
      console.warn('Error fetching general-information:', userInfoResult.reason?.message);
    }

    let dashData = null;
    if (dashDataResult.status === 'fulfilled') {
      dashData = dashDataResult.value;
    } else {
      console.warn('Error fetching dashboard data, falling back to mock:', dashDataResult.reason?.message);
    }
    
    let activeSeller;
    if (dashData) {
      activeSeller = adaptDashboardData(dashData);
      if (userInfo) {
        activeSeller.user_name = userInfo.user_name;
        activeSeller.nombre_tienda = userInfo.nombre_tienda;
        activeSeller.email = userInfo.email;
      }
      state.sellers = { [activeSeller.id]: activeSeller };
      state.selectedSellerId = activeSeller.id;
      state.usingMockData = false;
    } else {
      console.warn('[DiME] Usando datos mock debido a fallo en la API');
      state.sellers = MOCK_SELLERS;
      state.selectedSellerId = Number(Object.keys(MOCK_SELLERS)[0]);
      activeSeller = state.sellers[state.selectedSellerId];
      state.usingMockData = true;
    }
    
    updateDashboard(state.selectedSellerId);
  } catch (err) {
    document.getElementById('loadingSpinner').innerHTML = `
      <div class="error-message">
        <p>Error: ${err.message}</p>
        <button onclick="loadDashboard()" class="btn-retry">Reintentar</button>
      </div>`;
  }
}

document.getElementById('user-profile-button').addEventListener('click', function(e) {
  e.stopPropagation();
  const m = document.getElementById('profile-dropdown-menu');
  m.style.display = m.style.display === 'none' ? 'block' : 'none';
});

document.addEventListener('click', () => {
  const m = document.getElementById('profile-dropdown-menu');
  if (m.style.display !== 'none') m.style.display = 'none';
});

document.getElementById('btn-signout').addEventListener('click', () => {
  localStorage.clear(); sessionStorage.clear(); window.location.href = '/';
});
document.getElementById('pub-search').addEventListener('input', applyFilters);
document.getElementById('pub-category-filter').addEventListener('change', applyFilters);

document.querySelectorAll('.sidebar nav .nav-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const viewTarget = this.getAttribute('data-view');
    if (!viewTarget) return;

    document.querySelectorAll('.sidebar nav .nav-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');

    document.querySelectorAll('.content-view').forEach(v => v.classList.remove('active'));
    document.getElementById(viewTarget)?.classList.add('active');

    if (this.id !== 'nav-diagnostico-parent') {
      document.getElementById('nav-diagnostico-subgroup')?.classList.remove('open');
      document.getElementById('nav-diagnostico-caret')?.classList.remove('open');
    }
  });
});

document.getElementById('nav-diagnostico-parent')?.addEventListener('click', function() {
  document.getElementById('nav-diagnostico-subgroup')?.classList.toggle('open');
  document.getElementById('nav-diagnostico-caret')?.classList.toggle('open');
});

document.querySelectorAll('.nav-subbtn').forEach(subBtn => {
  subBtn.addEventListener('click', function(e) {
    e.stopPropagation();

    document.querySelectorAll('.sidebar nav .nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('nav-diagnostico-parent')?.classList.add('active');
    document.querySelectorAll('.content-view').forEach(v => v.classList.remove('active'));
    document.getElementById('view-diagnostico')?.classList.add('active');

    document.querySelectorAll('.nav-subbtn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');

    const tabTarget = this.getAttribute('data-tab');
    document.querySelectorAll('.diag-sub-view').forEach(content => content.classList.remove('active'));
    document.getElementById(tabTarget)?.classList.add('active');
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const token = getToken();
  if (!token) console.warn('[DiME] Sin token — mostrando datos mock');
  loadDashboard();
  loadDiagnosticoEmbeds();
  loadDiagnosticoInsights();
  loadPlanAccionList();
});

// Theme toggle
var themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
  themeToggle.addEventListener('click', function() {
    var current = document.documentElement.getAttribute('data-theme');
    var next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
  if (!localStorage.getItem('theme')) {
    document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
  }
});

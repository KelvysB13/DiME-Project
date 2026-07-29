const API_URL = "/api";

const FEATURE_LABELS = {
    metricas_basicas: "Auditoría básica de métricas",
    metricas_avanzadas: "Auditoría automatizada",
    reporte_mensual: "Reportes mensuales",
    reporte_personalizado: "Reportes personalizados",
    exportar_datos: "Exportación de datos",
    soporte_prioritario: "Soporte prioritario",
    multi_cuenta: "Múltiples cuentas",
    api_acceso: "Acceso a API",
};

async function cargarPlanes() {
    const grid = document.getElementById("pricing-grid");
    if (!grid) return;

    try {
        const res = await fetch(`${API_URL}/plans`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        const planes = data.planes || [];

        const basicFeatures = planes[0]?.features || [];

        grid.innerHTML = planes
            .map((p, i) => {
                const isFeatured = i === planes.length - 1;

                let features;
                if (isFeatured) {
                    const premiumOnly = (p.features || []).filter(
                        (f) => !basicFeatures.includes(f)
                    );
                    features =
                        `<li>Todo lo que contiene el plan básico</li>` +
                        premiumOnly
                            .map((f) => `<li>${FEATURE_LABELS[f] || f}</li>`)
                            .join("");
                } else {
                    features = (p.features || [])
                        .map((f) => `<li>${FEATURE_LABELS[f] || f}</li>`)
                        .join("");
                }

                const badge = isFeatured
                    ? '<div class="pricing-badge">Más popular</div>'
                    : "";
                const btnText =
                    p.precio_mensual === 0
                        ? "Comenzar gratis"
                        : `Adquirir ${p.nombre_plan}`;
                return `
                    <div class="pricing-card ${isFeatured ? "pricing-card--featured" : ""}">
                        ${badge}
                        <div class="pricing-card-header">
                            <h3>${p.nombre_plan}</h3>
                            <p class="pricing-desc">${p.descripcion || ""}</p>
                        </div>
                        <div class="price">${p.precio_mensual === 0 ? "$0" : `$${p.precio_mensual.toFixed(0)}`}<span>/mes</span></div>
                        <ul>${features}</ul>
                        <a href="/auth/register" class="btn">${btnText}</a>
                    </div>
                `;
            })
            .join("");
    } catch {
        grid.innerHTML =
            '<p style="text-align:center;color:var(--text-muted);grid-column:1/-1;">No se pudieron cargar los planes.</p>';
    }
}

document.addEventListener("DOMContentLoaded", cargarPlanes);

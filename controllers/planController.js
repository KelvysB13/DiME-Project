// El diccionario de acciones, las combinaciones y calcularPlanFinal() viven en
// kpiActionsService.js (compartido con los mensajes de diagnóstico). Este archivo
// solo se encarga de armar el PDF a partir del resultado de calcularPlanFinal().

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

// --- LÓGICA PRINCIPAL ---
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

            const planFinal = calcularPlanFinal(dataKpis.items);

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

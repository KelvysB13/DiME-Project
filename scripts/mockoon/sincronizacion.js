// sincronizacion.js

// Esta función simula el Paso 3: Va a Mockoon y luego envía al mini-backend
async function iniciarSincronizacion() {
    try {
        console.log("🚀 [PASO 3] Iniciando Sincronización Experimental...");
        console.log("📡 Conectando con la API Mockoon (Puerto 3001)...");
        
        // Petición a tu Mock API (Asegúrate de tener Mockoon encendido en este puerto)
        const responseMockoon = await fetch('http://localhost:3001/api/vendedor/2');
        
        if (!responseMockoon.ok) {
            throw new Error(`Error en Mockoon: Status ${responseMockoon.status}`);
        }
        
        const datosVendedor = await responseMockoon.json();
        console.log("✅ Datos recibidos con éxito desde Mockoon:", datosVendedor);

        // [PASO 4] Envío al mini-backend puente hacia PostgreSQL
        console.log("📤 [PASO 4] Enviando JSON al mini-backend puente (Puerto 8080)...");
        
        const responseBackend = await fetch('http://localhost:8080/api/guardar-metricas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosVendedor)
        });

        if (!responseBackend.ok) {
            throw new Error(`El backend rechazó los datos: Status ${responseBackend.status}`);
        }

        console.log("🎉 [PASO 5] ¡Sincronización Completa! Los datos ya están en Postgres.");
        console.log("➡️ Próximo paso en flujo real: Redirigir a user_dashboard.html");

    } catch (error) {
        console.error("❌ ERROR EN EL FLUJO:", error.message);
        console.log("💡 Consejo: Verifica que Mockoon esté encendido y que el mini-backend esté corriendo.");
    }
}

// ====================================================================
// ACTIVACIÓN EXPERIMENTAL (Sin botones ni HTML)
// ====================================================================
// Este bloque ejecuta la función automáticamente 2 segundos después de cargar la página
// para darte tiempo de abrir la consola del navegador (F12) y ver el proceso en vivo.
window.addEventListener('DOMContentLoaded', () => {
    console.log("ℹ️ Archivo script cargado. Esperando 2 segundos para disparar la prueba...");
    setTimeout(iniciarSincronizacion, 2000);
});
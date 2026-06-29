// Atrapamos el botón directamente
const btnConnectML = document.getElementById('connectML');

if (btnConnectML) {
    btnConnectML.addEventListener('click', async (e) => {
        e.preventDefault(); // Evita que el formulario recargue la página

        // 1. Capturar los valores del formulario
        const nombreCompleto = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();
        const usuarioML = document.getElementById('usuario_ml').value.trim();

        if (!nombreCompleto || !email || !usuarioML) {
            alert("⚠️ Por favor, completa tu nombre, correo y usuario de ML antes de conectar.");
            return;
        }

        // 2. Generar el ID aleatorio (16 al 22)
        const min = 16;
        const max = 22;
        const idPlantilla = Math.floor(Math.random() * (max - min + 1)) + min;

        console.log("🚀 Iniciando conexión...");
        console.log("👤 Datos capturados:", { nombreCompleto, email, usuarioML });
        console.log("🎲 Buscando la Plantilla ID:", idPlantilla);

        try {
            // 3. Fetch a Mockoon (Asegúrate de que la ruta coincida con la tuya)
            const responseMock = await fetch(`http://localhost:3001/api/vendedor/${idPlantilla}`);
            
            if (!responseMock.ok) {
                throw new Error(`Mockoon respondió con error: ${responseMock.status}`);
            }
            
            const plantilla = await responseMock.json();

            // 4. Enriquecer los datos (Reemplazar los TEMPLATE_...)
            if (plantilla.datos_basicos) {
                plantilla.datos_basicos.user_name = usuarioML;
                plantilla.datos_basicos.nombre_tienda = nombreCompleto;
                plantilla.datos_basicos.email = email;
            } else {
                // Por si el JSON vino plano
                plantilla.user_name = usuarioML;
                plantilla.nombre_tienda = nombreCompleto;
                plantilla.email = email;
            }

            console.log("✅ JSON híbrido listo para el backend:", plantilla);

            // 5. Fetch al Backend en Python
            const responseBack = await fetch('http://localhost:8080/api/guardar-metricas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(plantilla)
            });

            if (responseBack.ok) {
                alert("✅ ¡Cuenta creada con éxito! Sincronización completa con PostgreSQL.");
                // window.location.href = '/views/dashboard.html'; // Descomenta esto cuando tengas tu dashboard
            } else {
                const errorData = await responseBack.json();
                throw new Error(errorData.error || "El backend rechazó los datos.");
            }

        } catch (error) {
            console.error("❌ Error en la tubería de datos:", error);
            alert("Fallo en la sincronización: " + error.message);
        }
    });
} else {
    console.error("❌ No se encontró el botón 'connectML'.");
}
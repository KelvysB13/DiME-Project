document.addEventListener('DOMContentLoaded', () => {
    const btnConnectML = document.getElementById('connectML');
    const btnRegistrar = document.getElementById('btnRegistrar');
    const registerForm = document.getElementById('registerForm');
    
    const modal = document.getElementById('oauthModal');
    const btnCancelAuth = document.getElementById('btnCancelAuth');
    const btnAcceptAuth = document.getElementById('btnAcceptAuth');
    const syncLoader = document.getElementById('syncLoader');

    let plantillaPreparada = null;
    let syncCancelado = false;

    // 1. ABRIR EL MODAL
    if (btnConnectML) {
        btnConnectML.addEventListener('click', (e) => {
            e.preventDefault();

            const nombreCompleto = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            const usuarioML = document.getElementById('usuario_ml').value.trim();

            if (!nombreCompleto || !email || !usuarioML) {
                alert("⚠️ Por favor, completa tu nombre, correo y usuario de ML antes de conectar.");
                return;
            }

            // Restaurar diseño inicial del modal
            btnAcceptAuth.style.display = 'block';
            syncLoader.style.display = 'none';
            syncCancelado = false; 

            modal.style.display = 'flex'; // Mostrar modal
        });
    }

    // 2. CANCELAR
    if (btnCancelAuth) {
        btnCancelAuth.addEventListener('click', () => {
            syncCancelado = true; 
            modal.style.display = 'none'; // Ocultar modal
        });
    }

    // 3. ACEPTAR AUTORIZACIÓN
    if (btnAcceptAuth) {
        btnAcceptAuth.addEventListener('click', async () => {
            // Mostrar spinner y ocultar botón
            btnAcceptAuth.style.display = 'none';
            syncLoader.style.display = 'block';
            syncCancelado = false;

            const nombreCompleto = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            const usuarioML = document.getElementById('usuario_ml').value.trim();

            const min = 16;
            const max = 22;
            const idPlantilla = Math.floor(Math.random() * (max - min + 1)) + min;

            try {
                // Simulación de carga
                await new Promise(resolve => setTimeout(resolve, 2500));

                if (syncCancelado) return; 

                // Fetch a Mockoon
                console.log(`Intentando conectar a Mockoon en el ID ${idPlantilla}...`);
                const responseMock = await fetch(`http://localhost:3001/api/vendedor/${idPlantilla}`);
                
                if (!responseMock.ok) throw new Error(`Error HTTP: ${responseMock.status}`);
                
                const plantilla = await responseMock.json();
                console.log("Datos de Mockoon recibidos correctamente.");

                if (plantilla.datos_basicos) {
                    plantilla.datos_basicos.user_name = usuarioML;
                    plantilla.datos_basicos.nombre_tienda = nombreCompleto;
                    plantilla.datos_basicos.email = email;
                } else {
                    plantilla.user_name = usuarioML;
                    plantilla.nombre_tienda = nombreCompleto;
                    plantilla.email = email;
                }

                plantillaPreparada = plantilla;
                modal.style.display = 'none';

                // Cambiar botón de conexión
                btnConnectML.innerHTML = `<span>✓</span> Sincronizado: ${usuarioML}`;
                btnConnectML.style.backgroundColor = '#10B981';
                btnConnectML.style.color = '#fff';
                btnConnectML.style.border = 'none';
                btnConnectML.style.pointerEvents = 'none';

                // ¡DESBLOQUEAR BOTÓN DE REGISTRO!
                console.log("Desbloqueando botón de registro...");
                btnRegistrar.disabled = false;
                btnRegistrar.style.opacity = '1';
                btnRegistrar.style.cursor = 'pointer';

            } catch (error) {
                if (!syncCancelado) {
                    console.error("❌ Error en la sincronización:", error);
                    alert("No se pudo conectar. ¿Mockoon está encendido en el puerto 3001?");
                    modal.style.display = 'none';
                }
            }
        });
    }

    // 4. REGISTRO FINAL (FETCH A PYTHON)
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!plantillaPreparada) {
                alert("⚠️ Debes autorizar la conexión con Mercado Libre primero.");
                return;
            }

            const originalText = btnRegistrar.innerHTML;
            btnRegistrar.innerHTML = 'Creando entorno...';
            btnRegistrar.disabled = true;

            try {
                const responseBack = await fetch('http://localhost:8080/api/guardar-metricas', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(plantillaPreparada)
                });

                if (responseBack.ok) {
                    alert("✅ ¡Cuenta creada con éxito!");
                    // window.location.href = '/views/dashboard.html'; 
                } else {
                    const errorData = await responseBack.json();
                    throw new Error(errorData.error || "El backend rechazó los datos.");
                }

            } catch (error) {
                console.error("❌ Error al guardar en BD:", error);
                alert("Fallo al crear la cuenta: " + error.message);
                btnRegistrar.innerHTML = originalText;
                btnRegistrar.disabled = false;
            }
        });
    }
});
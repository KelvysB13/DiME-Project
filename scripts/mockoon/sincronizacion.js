document.addEventListener('DOMContentLoaded', () => {
    
    // --- VARIABLES DE ESTADO Y CONFIGURACIÓN ---
    const API_FASTAPI = 'http://127.0.0.1:8000/api'; // Ajusta esto según el prefijo de tus rutas en FastAPI
    const API_PYTHON_METRICAS = 'http://localhost:8080/api';
    const API_MOCKOON = 'http://localhost:3001/api';

    let preTokenGlobal = null;
    let usuarioMLGlobal = null;
    let syncCancelado = false;

    // --- ELEMENTOS DEL DOM ---
    const step1 = document.getElementById('step-1-register');
    const step2 = document.getElementById('step-2-payment');
    const step3 = document.getElementById('step-3-connect');
    const mensajeDiv = document.getElementById('mensaje');
    const modal = document.getElementById('oauthModal');

    // Botones
    const btnContinuar = document.getElementById('btnContinuarRegistro');
    const btnGuardarPago = document.getElementById('btnGuardarPago');
    const btnConnectML = document.getElementById('btnConnectML');
    const btnCancelAuth = document.getElementById('btnCancelAuth');
    const btnAcceptAuth = document.getElementById('btnAcceptAuth');
    const syncLoader = document.getElementById('syncLoader');

    // Función auxiliar para mensajes
    const mostrarMensaje = (texto, color) => {
        mensajeDiv.style.display = 'block';
        mensajeDiv.style.color = color;
        mensajeDiv.innerText = texto;
    };

    // ==========================================
    // FASE 1: REGISTRO BÁSICO
    // ==========================================
    btnContinuar.addEventListener('click', async () => {
        const nombre_tienda = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const usuarioML = document.getElementById('usuario_ml').value.trim();

        if (!nombre_tienda || !email || !password || !usuarioML) {
            mostrarMensaje("⚠️ Completa todos los campos.", "red");
            return;
        }

        // Validación estricta impuesta por Pydantic (schemas.py)
        if (password.length < 12) {
            mostrarMensaje("⚠️ La contraseña debe tener al menos 12 caracteres.", "red");
            return;
        }

        const textoOriginal = btnContinuar.innerHTML;
        btnContinuar.innerHTML = 'Verificando...';
        btnContinuar.disabled = true;

        try {
            // Nota: Verifica si tu ruta real es /register o /auth/register
            const response = await fetch(`${API_FASTAPI}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre_tienda, email, password })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Error en el registro.");
            }

            const data = await response.json();
            
            // Guardamos el token y el usuario para las siguientes fases
            preTokenGlobal = data.pre_token;
            usuarioMLGlobal = usuarioML;

            mensajeDiv.style.display = 'none'; // Limpiar mensajes
            
            // Transición a Fase 2
            step1.style.display = 'none';
            step2.style.display = 'block';

        } catch (error) {
            mostrarMensaje(error.message, "red");
            btnContinuar.innerHTML = textoOriginal;
            btnContinuar.disabled = false;
        }
    });

    // ==========================================
    // FASE 2: MÉTODO DE PAGO
    // ==========================================
    btnGuardarPago.addEventListener('click', async () => {
        const nombre_titular = document.getElementById('nombre_titular').value.trim();
        const numero_tarjeta = document.getElementById('numero_tarjeta').value.trim();
        const mes = document.getElementById('mes_caducidad').value;
        const anio = document.getElementById('anio_caducidad').value;
        const cvv = document.getElementById('cvv').value.trim();

        if (!nombre_titular || numero_tarjeta.length !== 16 || !mes || !anio || cvv.length !== 3) {
            mostrarMensaje("⚠️ Revisa los datos. La tarjeta requiere 16 dígitos y CVV de 3.", "red");
            return;
        }

        const textoOriginal = btnGuardarPago.innerHTML;
        btnGuardarPago.innerHTML = 'Procesando pago...';
        btnGuardarPago.disabled = true;

        try {
            // Convertimos mes y año a enteros estandarizados como pide Pydantic
            const payload = {
                nombre_titular: nombre_titular,
                numero_tarjeta: numero_tarjeta,
                mes_caducidad: parseInt(mes, 10),
                anio_caducidad: parseInt(anio, 10),
                cvv: cvv
            };

            const response = await fetch(`${API_FASTAPI}/auth/method`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${preTokenGlobal}` // Inyección del Token de la Fase 1
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Tarjeta rechazada.");
            }

            mensajeDiv.style.display = 'none';

            // Transición a Fase 3
            step2.style.display = 'none';
            step3.style.display = 'block';

        } catch (error) {
            mostrarMensaje(error.message, "red");
            btnGuardarPago.innerHTML = textoOriginal;
            btnGuardarPago.disabled = false;
        }
    });

    // ==========================================
    // FASE 3: CONEXIÓN MERCADO LIBRE
    // ==========================================
    btnConnectML.addEventListener('click', (e) => {
        e.preventDefault();
        btnAcceptAuth.style.display = 'block';
        syncLoader.style.display = 'none';
        syncCancelado = false; 
        modal.style.display = 'flex';
    });

    btnCancelAuth.addEventListener('click', () => {
        syncCancelado = true; 
        modal.style.display = 'none';
    });

    btnAcceptAuth.addEventListener('click', async () => {
        btnAcceptAuth.style.display = 'none';
        syncLoader.style.display = 'block';
        syncCancelado = false;

        const nombreCompleto = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();

        // ID Aleatorio para la simulación
        const min = 16;
        const max = 22;
        const idPlantilla = Math.floor(Math.random() * (max - min + 1)) + min;

        try {
            await new Promise(resolve => setTimeout(resolve, 2500));
            if (syncCancelado) return; 

            // 1. Fetch a Mockoon
            const responseMock = await fetch(`${API_MOCKOON}/vendedor/${idPlantilla}`);
            if (!responseMock.ok) throw new Error("Fallo Mockoon");
            
            const plantilla = await responseMock.json();

            // Inyectamos datos recolectados (Nota: la contraseña real ya está en la BD por la Fase 1)
            // Aquí enviamos la contraseña quemada solo si el puerto 8080 la sigue exigiendo por NOT NULL
            const passTemporal = document.getElementById('password').value;

            if (plantilla.datos_basicos) {
                plantilla.datos_basicos.user_name = usuarioMLGlobal;
                plantilla.datos_basicos.nombre_tienda = nombreCompleto;
                plantilla.datos_basicos.email = email;
                plantilla.datos_basicos.password = passTemporal; 
            } else {
                plantilla.user_name = usuarioMLGlobal;
                plantilla.nombre_tienda = nombreCompleto;
                plantilla.email = email;
                plantilla.password = passTemporal;
            }

            // 2. Fetch a Python 8080
            const responseMetricas = await fetch(`${API_PYTHON_METRICAS}/guardar-metricas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(plantilla)
            });

            if (!responseMetricas.ok) throw new Error("Fallo al guardar métricas en DB.");

            modal.style.display = 'none';
            btnConnectML.innerHTML = `<span>✓</span> Tienda Sincronizada`;
            btnConnectML.style.backgroundColor = '#10B981';
            btnConnectML.style.pointerEvents = 'none';
            
            mostrarMensaje("Redirigiendo a tu Dashboard...", "green");
            setTimeout(() => window.location.href = '/auth/login', 1500);

        } catch (error) {
            if (!syncCancelado) {
                console.error(error);
                alert("Error crítico en la sincronización.");
                modal.style.display = 'none';
            }
        }
    });
});
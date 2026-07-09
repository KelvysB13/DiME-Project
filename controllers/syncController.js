document.addEventListener('DOMContentLoaded', () => {
    const API_FASTAPI = 'http://127.0.0.1:8000/api';
    const API_MOCKOON = 'http://localhost:3001/api';

    let syncCanceled = false;

    const modal = document.getElementById('oauthModal');
    const btnConnectML = document.getElementById('btnConnectML');
    const btnCancelAuth = document.getElementById('btnCancelAuth');
    const btnAcceptAuth = document.getElementById('btnAcceptAuth');
    const syncLoader = document.getElementById('syncLoader');
    const mensajeDiv = document.getElementById('mensaje');

    const showMessage = (text, color) => {
        mensajeDiv.style.display = 'block';
        mensajeDiv.style.color = color;
        mensajeDiv.innerText = text;
    };

    btnConnectML.addEventListener('click', (e) => {
        e.preventDefault();
        btnAcceptAuth.style.display = 'block';
        syncLoader.style.display = 'none';
        syncCanceled = false;
        modal.style.display = 'flex';
    });

    btnCancelAuth.addEventListener('click', () => {
        syncCanceled = true;
        modal.style.display = 'none';
    });

    btnAcceptAuth.addEventListener('click', async () => {
        btnAcceptAuth.style.display = 'none';
        syncLoader.style.display = 'block';
        syncCanceled = false;

        const usuarioML = document.getElementById('usuario_ml_hidden').value;
        const nombreTienda = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();

        const templateId = Math.floor(Math.random() * (22 - 16 + 1)) + 16;

        try {
            await new Promise((resolve) => setTimeout(resolve, 2500));
            if (syncCanceled) return;

            const mockRes = await fetch(`${API_MOCKOON}/vendedor/${templateId}`);
            if (!mockRes.ok) throw new Error('Mockoon respondió con HTTP ' + mockRes.status);

            const template = await mockRes.json();

            if (!template.datos_basicos) {
                throw new Error('La plantilla de Mockoon no contiene datos_basicos.');
            }

            template.datos_basicos.user_name = usuarioML;
            template.datos_basicos.nombre_tienda = nombreTienda;
            template.datos_basicos.email = email;
            delete template.datos_basicos.password;

            const metricsRes = await fetch(`${API_FASTAPI}/moockon-data`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(template),
            });

            if (!metricsRes.ok) {
                const errBody = await metricsRes.json().catch(() => ({}));
                throw new Error('Backend respondió: ' + (errBody.detail || 'HTTP ' + metricsRes.status));
            }

            modal.style.display = 'none';
            btnConnectML.innerHTML = '<span>✓</span> Tienda Sincronizada';
            btnConnectML.style.backgroundColor = '#10B981';
            btnConnectML.style.pointerEvents = 'none';

            showMessage('Redirigiendo a tu Dashboard...', 'green');
            setTimeout(() => (window.location.href = '/auth/login'), 1500);
        } catch (error) {
            if (!syncCanceled) {
                console.error('Error de sincronización:', error);
                showMessage('Error: ' + error.message, 'red');
                syncLoader.style.display = 'none';
                btnAcceptAuth.style.display = 'block';
            }
        }
    });
});

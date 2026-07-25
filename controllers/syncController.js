document.addEventListener('DOMContentLoaded', () => {
    const API_FASTAPI = '/api';

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

        const token = localStorage.getItem('access_token');
        if (!token) {
            showMessage('No hay sesión activa. Redirigiendo al login...', 'red');
            setTimeout(() => (window.location.href = '/auth/login'), 2000);
            return;
        }

        const usuarioML = document.getElementById('usuario_ml_hidden').value;

        try {
            await new Promise((resolve) => setTimeout(resolve, 1500));
            if (syncCanceled) return;

            const response = await fetch(`${API_FASTAPI}/payment/sync-mockoon`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ usuario_ml: usuarioML || undefined }),
            });

            if (!response.ok) {
                const errBody = await response.json().catch(() => ({}));
                throw new Error(errBody.detail || 'Error al sincronizar con Mockoon');
            }

            modal.style.display = 'none';
            btnConnectML.innerHTML = '<span>✓</span> Tienda Sincronizada';
            btnConnectML.style.backgroundColor = '#10B981';
            btnConnectML.style.pointerEvents = 'none';

            showMessage('Redirigiendo a tu Dashboard...', 'green');
            setTimeout(() => (window.location.href = '/me/dashboard'), 1500);
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
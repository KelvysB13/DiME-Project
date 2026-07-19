function detectCardBrand(value) {
    const raw = value.replace(/\s/g, '');
    const brandEl = document.getElementById('cardBrand');
    if (!raw) { brandEl.innerHTML = ''; return; }

    const first = raw[0];
    const firstTwo = parseInt(raw.slice(0, 2), 10);
    const firstFour = parseInt(raw.slice(0, 4), 10);

    if (first === '4') {
        brandEl.innerHTML = '<img src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Visa_Inc._logo_%282021%E2%80%93present%29.svg" alt="Visa" height="18">';
    } else if ((firstTwo >= 51 && firstTwo <= 55) || (firstFour >= 2221 && firstFour <= 2720)) {
        brandEl.innerHTML = '<img src="https://upload.wikimedia.org/wikipedia/commons/a/a4/Mastercard_2019_logo.svg" alt="Mastercard" height="18">';
    } else {
        brandEl.innerHTML = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('togglePassword').addEventListener('click', function () {
        const password = document.getElementById('password');
        const icon = document.getElementById('eyeIcon');

        if (password.type === 'password') {
            password.type = 'text';
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"/>';
        } else {
            password.type = 'password';
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>';
        }
    });

    const text = "Crece tu negocio \nhoy mismo.";
    const el = document.getElementById('typewriter-text');
    let i = 0;
    let deleting = false;

    function typeWriter() {
        if (!deleting) {
            if (i < text.length) {
                el.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 55 + Math.random() * 45);
            } else {
                deleting = true;
                setTimeout(typeWriter, 1500);
            }
        } else {
            if (i > 0) {
                el.textContent = text.substring(0, i - 1);
                i--;
                setTimeout(typeWriter, 30 + Math.random() * 25);
            } else {
                deleting = false;
                setTimeout(typeWriter, 500);
            }
        }
    }

    setTimeout(() => typeWriter(), 400);

    const API_FASTAPI = '/api';
    const mensajeDiv = document.getElementById('mensaje');
    const step1 = document.getElementById('step-1-register');
    const step2 = document.getElementById('step-2-payment');

    const showMessage = (text, color) => {
        mensajeDiv.style.display = 'block';
        mensajeDiv.style.color = color;
        mensajeDiv.innerText = text;
    };

    window.handleRegister = async () => {
        const nombre_tienda = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const usuarioML = document.getElementById('usuario_ml').value.trim();
        const btn = document.getElementById('btnContinuarRegistro');

        if (!nombre_tienda || !email || !password || !usuarioML) {
            showMessage('Completa todos los campos.', 'red');
            return;
        }

        if (password.length < 12) {
            showMessage('La contraseña debe tener al menos 12 caracteres.', 'red');
            return;
        }

        const originalText = btn.innerHTML;
        btn.innerHTML = 'Verificando...';
        btn.disabled = true;

        try {
            const response = await fetch(`${API_FASTAPI}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre_tienda, email, password, usuario_ml: usuarioML }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                const detail = Array.isArray(errorData.detail)
                    ? errorData.detail.map((e) => e.msg).join('; ')
                    : errorData.detail || 'Error en el registro.';
                throw new Error(detail);
            }

            const data = await response.json();

            document.getElementById('pre_token').value = data.pre_token;
            document.getElementById('usuario_ml_hidden').value = usuarioML;

            mensajeDiv.style.display = 'none';
            step1.style.display = 'none';
            step2.style.display = 'block';
        } catch (error) {
            showMessage(error.message, 'red');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    };

    if (location.search.includes('dev')) {
        document.getElementById('nombre').value = 'TestTienda';
        document.getElementById('email').value = 'test@example.com';
        document.getElementById('password').value = 'TestPassword123';
        document.getElementById('usuario_ml').value = 'test_ml_user';
        document.getElementById('nombre_titular').value = 'Test User';
        document.getElementById('numero_tarjeta').value = '4111 1111 1111 1111';
        document.getElementById('mes_caducidad').value = 12;
        document.getElementById('anio_caducidad').value = 28;
        document.getElementById('cvv').value = '123';

        if (location.search.includes('dev-step2')) {
            document.getElementById('pre_token').value = 'dev_pre_token_123';
            document.getElementById('usuario_ml_hidden').value = 'test_ml_user';
            document.getElementById('step-1-register').style.display = 'none';
            document.getElementById('step-2-payment').style.display = 'block';
        }
    }
});

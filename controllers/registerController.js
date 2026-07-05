const API_URL = "http://127.0.0.1:8000/api";

function clearErrors()
{
    document.querySelectorAll('.form-group').forEach(g => g.classList.remove('error'));
    document.querySelectorAll('.field-error').forEach(e => { e.textContent = ''; e.classList.remove('visible'); });
    document.getElementById('mensaje').style.display = 'none';
}

function showFieldError(fieldId)
{
    const group = document.getElementById(fieldId + '-group');
    if (group) group.classList.add('error');
}

document.getElementById('registerForm').addEventListener('submit', async (e) => {

    e.preventDefault();
    clearErrors();

    const nombre_tienda = document.getElementById('nombre').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const mensajeDiv = document.getElementById('mensaje');
    let hasError = false;

    if (!nombre_tienda)
    {
        showFieldError('nombre');
        hasError = true;
    }

    if (!email)
    {
        showFieldError('email');
        hasError = true;
    }

    if (!password || password.length < 6)
    {
        showFieldError('password');
        hasError = true;
    }

    if (hasError) return;

    try
    {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre_tienda, email, password })
        });

        if (response.ok)
        {
            mensajeDiv.style.display = 'block';
            mensajeDiv.style.color = "green";
            mensajeDiv.innerText = 'Usuario registrado exitosamente. Redirigiendo...';
            setTimeout(() => window.location.href = '/auth/login', 1500);
        }
        else if (response.status === 409)
        {
            showFieldError('email');
            mensajeDiv.style.display = 'block';
            mensajeDiv.style.color = "red";
            mensajeDiv.innerText = 'El correo electrónico ya está registrado.';
        }
        else if (response.status === 422)
        {
            mensajeDiv.style.display = 'block';
            mensajeDiv.style.color = "red";
            mensajeDiv.innerText = 'Datos inválidos. Verifica los campos.';
        }
        else
        {
            mensajeDiv.style.display = 'block';
            mensajeDiv.style.color = "red";
            mensajeDiv.innerText = 'Error al registrar. Intenta de nuevo.';
        }
    }
    catch (error)
    {
        console.error('Error:', error);
        mensajeDiv.style.display = 'block';
        mensajeDiv.style.color = "red";
        mensajeDiv.innerText = "Error de conexión con el servidor.";
    }
});

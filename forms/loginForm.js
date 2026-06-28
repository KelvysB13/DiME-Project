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

document.getElementById('loginForm').addEventListener('submit', async (e) => {

    e.preventDefault();
    clearErrors();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const mensajeDiv = document.getElementById('mensaje');
    let hasError = false;

    if (!email) 
    {
        showFieldError('email');
        hasError = true;
    }

    if (!password) 
    {
        showFieldError('password');
        hasError = true;
    }

    if (hasError) return;

    try 
    {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {

                'Content-Type': 'application/json'
            },

            body: JSON.stringify({ email, password })
        });

        if (response.ok) 
        {
            const data = await response.json().catch(() => ({}));
            if (data && data.access_token) localStorage.setItem('token', data.access_token);
            window.location.href = '/me/dashboard';
        } 
        
        else 
        {
            showFieldError('email');
            showFieldError('password');
            mensajeDiv.style.display = 'block';
            mensajeDiv.style.color = "red";
            mensajeDiv.innerText = 'Credenciales Inválidas. *';
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

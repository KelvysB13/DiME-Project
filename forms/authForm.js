const API_URL = "http://127.0.0.1:8000/api";

async function renovarAccessToken() 
{
    // 1. Obtener el refresh token guardado
    const refreshTokenActual = localStorage.getItem('refresh_token');
    
    if (!refreshTokenActual) 
    {
        // No hay forma de renovar, hay que mandarlo al login
        window.location.href = 'index.html';
        return null;
    }

    try 
    {
        // 2. Enviar la solicitud cumpliendo con TokenRequest
        const response = await fetch(`${API_URL}/auth/refresh`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                refresh_token: refreshTokenActual
            })
        });

        const data = await response.json();

        if (response.ok) 
        {
            // 3. Procesar TokenResponse
            // access_token, token_type ("bearer"), expires_in
            localStorage.setItem('token', data.access_token);
            console.log(`Token renovado. Expira en: ${data.expires_in} segundos.`);
            
            return data.access_token;
        } 

        else 
        {
            // Si el refresh_token también expiró o es inválido
            console.error("El refresh token no es válido:", data.detail);
            localStorage.clear(); // Limpia sesión antigua
            window.location.href = 'index.html';
            return null;
        }

    } 
    
    catch (error) 
    {
        console.error("Error de red intentando renovar el token:", error);
        return null;
    }
}
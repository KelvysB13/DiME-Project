const API_URL = "http://127.0.0.1:8000/api";

async function renovarAccessToken() 
{
    // 1. Obtener el refresh token guardado
    const refreshTokenActual = localStorage.getItem('refresh_token');
    
    if (!refreshTokenActual) 
    {
        // No hay forma de renovar, hay que mandarlo al login
        window.location.href = '/auth/login';
        return null;
    }

    try 
    {
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
            localStorage.setItem('token', data.access_token);
            return data.access_token;
        } 

        else 
        {
            console.error("El refresh token no es válido:", data.detail);
            localStorage.clear();
            window.location.href = '/auth/login';
            return null;
        }

    } 
    
    catch (error) 
    {
        console.error("Error de red intentando renovar el token:", error);
        return null;
    }
}
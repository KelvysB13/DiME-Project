const API_FASTAPI = '/api';

document.addEventListener('DOMContentLoaded', () => {

    const btnGuardarPago = document.getElementById('btnGuardarPago');
    const mensajeDiv = document.getElementById('mensaje');
    const step2 = document.getElementById('step-2-payment');
    const step3 = document.getElementById('step-3-connect');

    const showMessage = (text, color) => {

        mensajeDiv.style.display = 'block';
        mensajeDiv.style.color = color;
        mensajeDiv.innerText = text;
    };

    window.handlePayment = async () => {

        const preToken = document.getElementById('pre_token').value;
        const nombre_titular = document.getElementById('nombre_titular').value.trim();
        const numero_tarjeta = document.getElementById('numero_tarjeta').value.replace(/\s/g, '');
        const mes = document.getElementById('mes_caducidad').value;
        const anio = document.getElementById('anio_caducidad').value;
        const cvv = document.getElementById('cvv').value.trim();

        if (!preToken) {

            showMessage('Completa primero el registro.', 'red');
            return;
        }

        if (!nombre_titular || numero_tarjeta.length !== 16 || !mes || !anio || cvv.length !== 3) {

            showMessage('Revisa los datos. La tarjeta requiere 16 dígitos y CVV de 3.', 'red');
            return;
        }

        const originalText = btnGuardarPago.innerHTML;
        btnGuardarPago.innerHTML = 'Procesando pago...';
        btnGuardarPago.disabled = true;

        try 
        {

            const payload = {

                pre_token: preToken,
                id_plan: 2,
                nombre_titular,
                numero_tarjeta,
                mes_caducidad: parseInt(mes, 10),
                anio_caducidad: parseInt(anio, 10),
                cvv,
            };

            const response = await fetch(`${API_FASTAPI}/payment/checkout`, {

                method: 'POST',
                headers: {

                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${preToken}`,
                },

                body: JSON.stringify(payload),
            });

            if (!response.ok) 
            {

                const errorData = await response.json();
                throw new Error(errorData.detail || 'Tarjeta rechazada.');
            }

            mensajeDiv.style.display = 'none';
            step2.style.display = 'none';
            step3.style.display = 'block';

            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 2500);
        } 
        
        catch (error) 
        {
            showMessage(error.message, 'red');
            btnGuardarPago.innerHTML = originalText;
            btnGuardarPago.disabled = false;
        }
    };
});

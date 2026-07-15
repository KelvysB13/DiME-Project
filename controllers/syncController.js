document.addEventListener('DOMContentLoaded', () => {
    const step3 = document.getElementById('step-3-connect');
    if (step3) {
        setTimeout(() => {
            window.location.href = '/auth/login';
        }, 2500);
    }
});

/* Style pour connexion_etudiant.html */
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('.login-form');
    const submitBtn = document.querySelector('.btn-login');

    if (loginForm && submitBtn) {
        loginForm.addEventListener('submit', function () {
            // Effet visuel au clic sur le bouton pour feedback utilisateur
            submitBtn.style.opacity = '0.7';
            submitBtn.innerText = '⏳...';
        });
    }
});
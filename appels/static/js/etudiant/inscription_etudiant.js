/* Style pour inscription_etudiant.html */
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-inscription');

    if (form) {
        form.addEventListener('submit', function (event) {
            // Récupère le message traduit dynamiquement transmis par le template HTML
            const confirmMessage = form.getAttribute('data-confirm-message');
            
            if (!confirm(confirmMessage)) {
                event.preventDefault(); // Annule l'envoi du formulaire si l'utilisateur annule
            }
        });
    }
    
});
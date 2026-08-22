document.addEventListener("DOMContentLoaded", function () {
    // Focus automatique sur le champ de saisie du code à l'ouverture
    const codeInput = document.querySelector('.verify-form input[type="text"]');
    
    if (codeInput) {
        codeInput.focus();
        
        // Empêche la saisie de caractères non numériques si désiré
        codeInput.addEventListener('input', function (e) {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});
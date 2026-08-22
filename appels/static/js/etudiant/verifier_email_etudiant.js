document.addEventListener("DOMContentLoaded", function () {
    const codeInput = document.querySelector('.verify-form input[type="text"]');
    
    if (codeInput) {
        codeInput.focus();
        
        // Autoriser uniquement les chiffres
        codeInput.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});
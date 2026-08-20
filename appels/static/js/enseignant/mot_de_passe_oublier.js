/* Style pour mot_de_passe_oublier.html */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-reset-password");
    const submitBtn = form ? form.querySelector(".btn-submit") : null;

    if (form) {
        form.addEventListener("submit", function () {
            // Empêche le double-clic lors de l'envoi du mail
            if (submitBtn) {
                submitBtn.style.opacity = "0.7";
                submitBtn.style.pointerEvents = "none";
            }
        });
    }
});
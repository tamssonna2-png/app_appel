/* Style pour connexion.html */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-connexion-enseignant");
    const submitBtn = form.querySelector(".btn-login");

    form.addEventListener("submit", function () {
        // Désactive le bouton pour éviter les double clics sur mobile
        if (submitBtn) {
            submitBtn.style.opacity = "0.7";
            submitBtn.style.pointerEvents = "none";
        }
    });
});
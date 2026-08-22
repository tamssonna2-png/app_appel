/* Style pour inscription_enseignant.html */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-inscription-enseignant");
    const submitBtn = form ? form.querySelector(".btn-submit") : null;

    if (form) {
        form.addEventListener("submit", function () {
            // Évite la soumission multiple lors de l'appui sur mobile
            if (submitBtn) {
                submitBtn.style.opacity = "0.7";
                submitBtn.style.pointerEvents = "none";
            }
        });
    }
});
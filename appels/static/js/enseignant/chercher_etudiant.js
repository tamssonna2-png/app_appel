/* Style pour chercher_etudiant.html */
document.addEventListener("DOMContentLoaded", function () {
    const formEnroll = document.getElementById("form-enroll-student");

    if (formEnroll) {
        const submitBtn = formEnroll.querySelector(".btn-enroll");
        formEnroll.addEventListener("submit", function () {
            // Empêche les soumissions multiples sur mobile lors de l'inscription
            if (submitBtn) {
                submitBtn.style.opacity = "0.7";
                submitBtn.style.pointerEvents = "none";
            }
        });
    }
});
/* Style pour verifier_code_recuperation.html */
document.addEventListener("DOMContentLoaded", function () {
    const formCode = document.getElementById("form-verify-code");
    const formPassword = document.getElementById("form-new-password");

    // Gestion du formulaire de code
    if (formCode) {
        const submitBtnCode = formCode.querySelector(".btn-submit");
        formCode.addEventListener("submit", function () {
            if (submitBtnCode) {
                submitBtnCode.style.opacity = "0.7";
                submitBtnCode.style.pointerEvents = "none";
            }
        });
    }

    // Gestion du formulaire de nouveau mot de passe
    if (formPassword) {
        const submitBtnPassword = formPassword.querySelector(".btn-submit");
        formPassword.addEventListener("submit", function () {
            if (submitBtnPassword) {
                submitBtnPassword.style.opacity = "0.7";
                submitBtnPassword.style.pointerEvents = "none";
            }
        });
    }
});
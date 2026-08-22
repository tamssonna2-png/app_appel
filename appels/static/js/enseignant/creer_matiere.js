/* Style pour creer_matiere.html */
// Bascule d'affichage des champs de pondération
function toggleInputs() {
    const check = document.getElementById('checkPonderation');
    const inputs = document.getElementById('inputsPonderation');
    
    if (check && inputs) {
        inputs.style.display = check.checked ? 'flex' : 'none';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-create-subject");

    if (form) {
        const submitBtn = form.querySelector(".btn-submit");
        form.addEventListener("submit", function () {
            // Empêche le double-clic à l'envoi
            if (submitBtn) {
                submitBtn.style.opacity = "0.7";
                submitBtn.style.pointerEvents = "none";
            }
        });
    }
});

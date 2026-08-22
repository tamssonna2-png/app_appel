/* Style pour supprimer_matiere.html */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-supprimer-matiere");
    const btnDelete = document.getElementById("btn-confirm-delete");

    if (form && btnDelete) {
        form.addEventListener("submit", function (event) {
            // Confirmation de sécurité JS supplémentaire
            const confirmation = confirm("Cette action est définitive. Êtes-vous sûr de vouloir supprimer cette matière ?");
            if (!confirmation) {
                event.preventDefault();
                return;
            }

            // Verrouillage du bouton pendant l'envoi
            btnDelete.disabled = true;
            btnDelete.style.opacity = "0.7";
            btnDelete.innerHTML = "Suppression...";
        });
    }
});
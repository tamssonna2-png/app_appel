/* Style pour dashboard_etudiant.html */
document.addEventListener('DOMContentLoaded', function () {

    // --- LOGIQUE DU TIMER ---
    function updateTimers() {
        // On récupère tous les timers de la page
        const timers = document.querySelectorAll('.timer');

        timers.forEach(timer => {
            let secondes = parseInt(timer.getAttribute('data-seconds'));

            if (secondes > 0) {
                secondes--;
                
                timer.setAttribute('data-seconds', secondes); // On met à jour la valeur stockée

                let mins = Math.floor(secondes / 60);
                let secs = secondes % 60;
                timer.innerText = mins + ":" + (secs < 10 ? "0" : "") + secs;
            } else {
                timer.innerText = "EXPIRÉ";
                // Optionnel : recharger la page pour faire disparaître le formulaire
                // window.location.reload(); 
            }
        });
    }

    // Lance la mise à jour toutes les secondes pour tous les timers trouvés
    setInterval(updateTimers, 1000);

    // --- LOGIQUE GEOLOCALISATION ET VALIDATION ---
    function validerAvecGPS(appelId, btn) {
        btn.innerText = "⏳...";
        btn.disabled = true;

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                document.getElementById('lat-' + appelId).value = position.coords.latitude;
                document.getElementById('lon-' + appelId).value = position.coords.longitude;
                document.getElementById('form-valider-' + appelId).submit();
            }, function (error) {
                alert("Erreur GPS : " + error.message + ". Validation impossible sans localisation.");
                btn.innerText = "Valider";
                btn.disabled = false;
            }, { enableHighAccuracy: true, timeout: 6000 });
        } else {
            alert("Géolocalisation non supportée.");
        }
    }

    // Attachement de l'événement click aux boutons de validation
    document.querySelectorAll('.btn-validate').forEach(button => {
        button.addEventListener('click', function (e) {
            const appelId = this.getAttribute('data-appel-id');
            validerAvecGPS(appelId, this);
        });
    });

});
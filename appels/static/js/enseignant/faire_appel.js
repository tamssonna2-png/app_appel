/* Style pour faire_appel.html */
document.addEventListener("DOMContentLoaded", function () {
    // 1. Gestion du compte à rebours
    const timerDisplay = document.getElementById('timer');
    if (timerDisplay) {
        let secondes = parseInt(timerDisplay.getAttribute('data-seconds'), 10);

        if (!isNaN(secondes) && secondes > 0) {
            const updateTimer = () => {
                if (secondes > 0) {
                    secondes--;
                    const mins = Math.floor(secondes / 60);
                    const secs = secondes % 60;
                    timerDisplay.innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
                } else {
                    timerDisplay.innerText = "EXSPIRÉ (veuillez actualiser la page)";
                    //location.reload();
                    location.reload();
                    //window.location.href = window.location.href;*/
                    clearInterval(timerInterval);
                }
            };

            updateTimer();
            const timerInterval = setInterval(updateTimer, 1000);
        }
    }

    // 2. Gestion du clic sur le bouton d'appel avec géolocalisation
    const btnStart = document.getElementById("btn-start-call");
    if (btnStart) {
        btnStart.addEventListener("click", capturerPositionProf);
    }
});

function capturerPositionProf(event) {
    const btn = event ? event.currentTarget : document.getElementById("btn-start-call");
    if (btn) {
        btn.innerText = "⏳ Localisation...";
        btn.disabled = true;
        btn.style.opacity = "0.7";
    }

    const form = document.getElementById('form-lancer-appel');

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                document.getElementById('lat_prof').value = position.coords.latitude;
                document.getElementById('lon_prof').value = position.coords.longitude;
                if (form) form.submit();
            },
            function (error) {
                alert("Erreur GPS : " + error.message + ". L'appel sera lancé sans géolocalisation.");
                if (form) form.submit();
            },
            {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            }
        );
    } else {
        alert("Géolocalisation non supportée par votre navigateur.");
        if (form) form.submit();
    }
}
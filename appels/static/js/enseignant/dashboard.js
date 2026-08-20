/* Style pour dashboard.html */
document.addEventListener("DOMContentLoaded", function () {
    // Animation au clic sur les actions du tableau de bord
    const actionButtons = document.querySelectorAll(".btn-icon");

    actionButtons.forEach((btn) => {
        btn.addEventListener("touchstart", function () {
            this.style.transform = "scale(0.92)";
        });
        btn.addEventListener("touchend", function () {
            this.style.transform = "scale(1)";
        });
    });
});
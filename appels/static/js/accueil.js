/* Style pour acceuil.html */
/**
 * ATTENDO - Logique d'interaction d'accueil
 */
document.addEventListener('DOMContentLoaded', () => {
    // Petit effet visuel d'interaction au survol des boutons d'accès
    const buttons = document.querySelectorAll('.action-grid .btn');

    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-1px)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
        });
    });
});
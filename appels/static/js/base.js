/* Style pour base.html */
/**
 * ATTENDO Mobile - Scripts d'interaction UI
 */
document.addEventListener('DOMContentLoaded', () => {
    // Évite le délai de double-tap au clic sur mobile
    const interactiveElements = document.querySelectorAll('a, button');

    interactiveElements.forEach(el => {
        el.addEventListener('touchstart', () => {}, { passive: true });
    });
});
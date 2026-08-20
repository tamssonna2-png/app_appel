/* Style pour base_etudiant.html */
/**
 * ATTENDO - Logique Mobile & Service Worker Étudiant
 */
document.addEventListener('DOMContentLoaded', () => {
    // Enregistrement du Service Worker PWA
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/sw.js')
                .then((registration) => {
                    console.log('SW Étudiant enregistré avec succès :', registration.scope);
                })
                .catch((error) => {
                    console.error('Échec de l\'enregistrement SW :', error);
                });
        });
    }

    // Amélioration du toucher réactif sur mobile
    const buttons = document.querySelectorAll('.btn, .btn-logout-yellow, a');
    buttons.forEach(btn => {
        btn.addEventListener('touchstart', () => {}, { passive: true });
    });
});
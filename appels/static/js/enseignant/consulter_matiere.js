/* Style pour consulter_matiere.html */

// Fonction pour copier le lien d'inscription
function copyLink() {
    const linkElement = document.getElementById("lien-inscription");
    if (!linkElement) return;

    const copyText = linkElement.innerText;
    
    navigator.clipboard.writeText(copyText).then(function() {
        alert("Lien copié dans le presse-papier ! Partagez-le avec vos étudiants.");
    }).catch(function(err) {
        console.error("Erreur lors de la copie du lien : ", err);
    });
}
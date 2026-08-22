/* Style pour consulter_feuille.html */
// Filtrage Présents / Absents / Tous avec gestion d'état visuel
function filtrerEtudiants(filtre) {
    const lignes = document.querySelectorAll('.ligne-etudiant');
    const btns = document.querySelectorAll('.btn-filter');

    // Mise à jour de l'état actif des boutons
    btns.forEach(btn => btn.classList.remove('active'));
    
    if (filtre === 'tous') {
        document.getElementById('btn-filter-all')?.classList.add('active');
    } else if (filtre === 'present') {
        document.getElementById('btn-filter-present')?.classList.add('active');
    } else if (filtre === 'absent') {
        document.getElementById('btn-filter-absent')?.classList.add('active');
    }

    // Affichage/Masquage des lignes
    lignes.forEach(ligne => {
        if (filtre === 'tous') {
            ligne.style.display = '';
        } else if (filtre === 'present') {
            ligne.style.display = ligne.classList.contains('is-present') ? '' : 'none';
        } else if (filtre === 'absent') {
            ligne.style.display = ligne.classList.contains('is-absent') ? '' : 'none';
        }
    });
}

// Recherche dynamique instantanée
function rechercherParNom() {
    const input = document.getElementById('rechercheNom').value.toUpperCase();
    const lignes = document.querySelectorAll('.ligne-etudiant');
    
    lignes.forEach(ligne => {
        const texte = ligne.innerText.toUpperCase();
        ligne.style.display = texte.includes(input) ? "" : "none";
    });
}

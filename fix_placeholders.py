"""
Corrige les msgstr dont les placeholders %(...)s ont été traduits par erreur
par auto_translate.py (Google Translate a traduit les noms de variables Python).

A lancer une seule fois depuis la racine du projet :
    python fix_placeholders.py
Puis recompiler :
    python manage.py compilemessages -i myglobalenv
"""
import polib

CORRECTIONS = {
    'en': {
        '%(etudiant)s inscrit en %(matiere)s':
            '%(etudiant)s registered in %(matiere)s',
        'La matière %(nom)s a été créée':
            'The subject %(nom)s has been created',
        'La matiere %(nom)s a été mise à jour':
            'The subject %(nom)s has been updated',
        'La matière %(nom)s a été réinitialisée : historique et étudiants effacés.':
            'The subject %(nom)s has been reset: history and students cleared.',
        '%(prenom)s est maintenant inscrit à %(nom)s':
            '%(prenom)s is now registered in %(nom)s',
        '%(prenom)s etait déja inscrit':
            '%(prenom)s was already registered',
        'Felicitations : tu es maintenant inscrire au cour de %(nom)s':
            'Congratulations: you are now registered for the %(nom)s course',
        'Tu es déja inscrit au cour de %(nom)s':
            'You are already registered for the %(nom)s course',
    },
    'es': {
        '%(etudiant)s inscrit en %(matiere)s':
            '%(etudiant)s matriculado en %(matiere)s',
        'La matière %(nom)s a été créée':
            'La asignatura %(nom)s ha sido creada',
        'La matiere %(nom)s a été mise à jour':
            'La asignatura %(nom)s ha sido actualizada',
        'La matière %(nom)s a été réinitialisée : historique et étudiants effacés.':
            'La asignatura %(nom)s ha sido reiniciada: historial y estudiantes borrados.',
        '%(prenom)s est maintenant inscrit à %(nom)s':
            '%(prenom)s ahora está inscrito en %(nom)s',
        '%(prenom)s etait déja inscrit':
            '%(prenom)s ya estaba inscrito',
        'Appel lancé ! Le code est : %(code)s':
            '¡Llamada iniciada! El código es: %(code)s',
        'Felicitations : tu es maintenant inscrire au cour de %(nom)s':
            'Felicidades: ahora estás inscrito en el curso de %(nom)s',
        'Tu es déja inscrit au cour de %(nom)s':
            'Ya estás inscrito en el curso de %(nom)s',
        "Tu es trop loin de l'enseignant (%(distance)sm). Signaler à l'enseignant en cas d'erreur":
            'Estás demasiado lejos del profesor (%(distance)sm). Informa al profesor en caso de error.',
    },
}

for lang, fixes in CORRECTIONS.items():
    path = f'locale/{lang}/LC_MESSAGES/django.po'
    po = polib.pofile(path)
    corrected = 0
    for entry in po:
        if entry.msgid in fixes:
            entry.msgstr = fixes[entry.msgid]
            corrected += 1
    po.save()
    print(f"[{lang}] {corrected}/{len(fixes)} entrées corrigées dans {path}")
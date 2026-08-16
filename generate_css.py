"""from pathlib import Path

# Définition des dossiers
TEMPLATES_DIR = Path("appels/templates/enseignant")
CSS_DIR = Path("appels/static/css/enseignant")

# Crée le dossier static/css/enseignant s'il n'existe pas encore
CSS_DIR.mkdir(parents=True, exist_ok=True)

# Vérification du dossier source
if not TEMPLATES_DIR.exists():
    print(
        f" Erreur : Le dossier source '{TEMPLATES_DIR}' n'a pas été trouvé."
    )
else:
    # Parcours de tous les fichiers .html dans templates/enseignant
    html_files = list(TEMPLATES_DIR.glob("*.html"))

    if not html_files:
        print(f" Aucun fichier .html trouvé dans '{TEMPLATES_DIR}'.")
    else:
        for html_file in html_files:
            # Remplace l'extension .html par .css
            css_filename = html_file.stem + ".css"
            css_filepath = CSS_DIR / css_filename

            # Crée le fichier .css s'il n'existe pas déjà
            if not css_filepath.exists():
                css_filepath.write_text(
                    f"/* Style pour {html_file.name} */\n"
                )
                print(f" Fichier créé : {css_filepath}")
            else:
                print(f"ℹ Déjà existant : {css_filepath}")

        print("\n Terminé ! Tous les fichiers CSS ont été générés.")








TEMPLATES_DIR = Path("appels/templates/etudiant")
CSS_DIR = Path("appels/static/css/etudiant")
CSS_DIR.mkdir(parents=True, exist_ok=True)

# Vérification du dossier source
if not TEMPLATES_DIR.exists():
    print(
        f" Erreur : Le dossier source '{TEMPLATES_DIR}' n'a pas été trouvé."
    )
else:
    # Parcours de tous les fichiers .html dans templates/enseignant
    html_files = list(TEMPLATES_DIR.glob("*.html"))

    if not html_files:
        print(f" Aucun fichier .html trouvé dans '{TEMPLATES_DIR}'.")
    else:
        for html_file in html_files:
            # Remplace l'extension .html par .css
            css_filename = html_file.stem + ".css"
            css_filepath = CSS_DIR / css_filename

            # Crée le fichier .css s'il n'existe pas déjà
            if not css_filepath.exists():
                css_filepath.write_text(
                    f"/* Style pour {html_file.name} */\n"
                )
                print(f" Fichier créé : {css_filepath}")
            else:
                print(f"ℹ Déjà existant : {css_filepath}")

        print("\n Terminé ! Tous les fichiers CSS ont été générés.")



























from pathlib import Path

# Définition des dossiers
TEMPLATES_DIR = Path("appels/templates/enseignant")
CSS_DIR = Path("appels/static/js/enseignant")

# Crée le dossier static/css/enseignant s'il n'existe pas encore
CSS_DIR.mkdir(parents=True, exist_ok=True)

# Vérification du dossier source
if not TEMPLATES_DIR.exists():
    print(
        f" Erreur : Le dossier source '{TEMPLATES_DIR}' n'a pas été trouvé."
    )
else:
    # Parcours de tous les fichiers .html dans templates/enseignant
    html_files = list(TEMPLATES_DIR.glob("*.html"))

    if not html_files:
        print(f" Aucun fichier .html trouvé dans '{TEMPLATES_DIR}'.")
    else:
        for html_file in html_files:
            # Remplace l'extension .html par .css
            css_filename = html_file.stem + ".js"
            css_filepath = CSS_DIR / css_filename

            # Crée le fichier .css s'il n'existe pas déjà
            if not css_filepath.exists():
                css_filepath.write_text(
                    f"/* Style pour {html_file.name} */\n"
                )
                print(f" Fichier créé : {css_filepath}")
            else:
                print(f"ℹ Déjà existant : {css_filepath}")

        print("\n Terminé ! Tous les fichiers CSS ont été générés.")








TEMPLATES_DIR = Path("appels/templates/etudiant")
CSS_DIR = Path("appels/static/js/etudiant")
CSS_DIR.mkdir(parents=True, exist_ok=True)

# Vérification du dossier source
if not TEMPLATES_DIR.exists():
    print(
        f" Erreur : Le dossier source '{TEMPLATES_DIR}' n'a pas été trouvé."
    )
else:
    # Parcours de tous les fichiers .html dans templates/enseignant
    html_files = list(TEMPLATES_DIR.glob("*.html"))

    if not html_files:
        print(f" Aucun fichier .html trouvé dans '{TEMPLATES_DIR}'.")
    else:
        for html_file in html_files:
            # Remplace l'extension .html par .css
            css_filename = html_file.stem + ".js"
            css_filepath = CSS_DIR / css_filename

            # Crée le fichier .css s'il n'existe pas déjà
            if not css_filepath.exists():
                css_filepath.write_text(
                    f"/* Style pour {html_file.name} */\n"
                )
                print(f" Fichier créé : {css_filepath}")
            else:
                print(f"ℹ Déjà existant : {css_filepath}")

        print("\n Terminé ! Tous les fichiers CSS ont été générés.")"""
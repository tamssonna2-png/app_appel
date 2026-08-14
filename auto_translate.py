import time
import polib
from deep_translator import GoogleTranslator
from pathlib import Path

def sanitize_entry(entry):
    """Nettoie TOUS les attributs potentiellement nuls pour éviter le crash de polib.save()."""
    for attr in ['msgid', 'msgstr', 'msgid_plural', 'comment', 'tcomment']:
        if hasattr(entry, attr) and getattr(entry, attr) is None:
            setattr(entry, attr, '')

def translate_po(file_path, target_lang='en'):
    try:
        po = polib.pofile(str(file_path))
    except Exception as e:
        print(f" Impossible d'ouvrir {file_path}: {e}")
        return

    translator = GoogleTranslator(source='fr', target=target_lang)
    count = 0
    print(f"--- Traitement pour [{target_lang}] ({file_path}) ---")

    # 1. Nettoyage global de sécurité avant de commencer
    for entry in po:
        sanitize_entry(entry)
    
    # Tentative d'assainissement de l'en-tête metadata si présente
    if hasattr(po, 'metadata_is_fallback'):
        sanitize_entry(po)

    # 2. Boucle de traduction avec sauvegarde continue
    for entry in po:
        if entry.msgid and not entry.msgstr:
            try:
                translated = translator.translate(entry.msgid)
                entry.msgstr = translated if translated else ""
                
                # Assainir et sauvegarder immédiatement sur le disque
                sanitize_entry(entry)
                po.save()
                
                count += 1
                print(f" [{target_lang}] ({count}) '{entry.msgid}' -> '{entry.msgstr}'")
                time.sleep(0.3)  # Pause anti-blocage Google
            except Exception as e:
                print(f" Erreur sur '{entry.msgid}': {e}")
                entry.msgstr = ""
                sanitize_entry(entry)
                try:
                    po.save()
                except Exception:
                    pass

    print(f" Terminé pour [{target_lang}] ! {count} nouvelles expressions traduites.\n")

if __name__ == '__main__':
    locale_dir = Path('locale')
    if not locale_dir.exists():
        print("Erreur: Le dossier 'locale' n'existe pas. Lance d'abord 'python manage.py makemessages'.")
    else:
        for lang_dir in locale_dir.iterdir():
            if lang_dir.is_dir():
                po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
                if po_file.exists():
                    lang_code = lang_dir.name
                    translate_po(po_file, target_lang=lang_code)
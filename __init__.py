from aqt import mw
from aqt.qt import QAction
from .config import get_api_key
from .ui import select_deck, select_fields, select_languages, show_progress_dialog
from .translator import translate_notes

# Function to translate fields
def translate_fields():
    api_key = get_api_key()
    if not api_key:
        return

    deck_name = select_deck()
    if not deck_name:
        return

    note_ids, fields = select_fields(deck_name)
    if not note_ids:
        return

    field_to_translate, target_field = fields
    source_lang, target_lang = select_languages(api_key)
    if not source_lang or not target_lang:
        return

    progress_dialog = show_progress_dialog(len(note_ids))

    translate_notes(api_key, note_ids, field_to_translate, target_field, source_lang, target_lang, progress_dialog)

    mw.reset()

# Add menu item to Anki
action = QAction("Translate Fields", mw)
action.triggered.connect(translate_fields)
mw.form.menuTools.addAction(action)

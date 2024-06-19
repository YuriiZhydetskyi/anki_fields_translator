import sys
import os
import time
from aqt.qt import QMessageBox
from aqt import mw
from .ui import update_progress

# Ensure the lib path is added to sys.path
addon_path = os.path.dirname(__file__)
lib_path = os.path.join(addon_path, 'lib')
sys.path.insert(0, lib_path)

import deepl

def translate_notes(api_key, note_ids, field_to_translate, target_field, source_lang, target_lang, progress_dialog):
    translator = deepl.Translator(api_key)
    break_translation = False
    start_time = time.time()

    for current, note_id in enumerate(note_ids, 1):
        if progress_dialog.wasCanceled():
            break_translation = True
            break
        note = mw.col.getNote(note_id)
        source_text = note[field_to_translate]
        if source_text:
            target_text = note[target_field]
            if target_text:  # Skip notes where the target field is already populated
                continue
            try:
                translated_text = translator.translate_text(source_text, source_lang=source_lang, target_lang=target_lang)
                note[target_field] = str(translated_text)
                note.flush()
            except Exception as e:
                QMessageBox.warning(mw, "Translation Error", f"Error translating note {note_id}: {str(e)}")
        
        update_progress(progress_dialog, current, len(note_ids), start_time)
    
    progress_dialog.close()
    if break_translation:
        QMessageBox.information(mw, "Translation Interrupted", "Translation was interrupted by the user.")
    else:
        QMessageBox.information(mw, "Translation Completed", "Translation completed successfully.")

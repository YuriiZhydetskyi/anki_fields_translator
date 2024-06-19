import sys
import os
import time
from aqt import mw
from aqt.qt import QInputDialog, QMessageBox, QProgressDialog, Qt

# Ensure the lib path is added to sys.path
addon_path = os.path.dirname(__file__)
lib_path = os.path.join(addon_path, 'lib')
sys.path.insert(0, lib_path)

import deepl

def select_deck():
    decks = mw.col.decks.allNames()
    deck_name, ok = QInputDialog.getItem(mw, "Select Deck", "Choose a deck:", decks, 0, False)
    if not ok or not deck_name:
        return None
    return deck_name

def select_fields(deck_name):
    note_ids = mw.col.find_notes(f'deck:"{deck_name}"')
    if not note_ids:
        QMessageBox.information(mw, "No Notes", f"No notes found in deck '{deck_name}'")
        return None, None

    fields = mw.col.models.fieldNames(mw.col.getNote(note_ids[0]).model())

    field_to_translate, ok = QInputDialog.getItem(mw, "Select Field to Translate", "Choose a field to translate:", fields, 0, False)
    if not ok or not field_to_translate:
        return None, None

    target_field, ok = QInputDialog.getItem(mw, "Select Target Field", "Choose a field to insert translations:", fields, 0, False)
    if not ok or not target_field:
        return None, None

    return note_ids, (field_to_translate, target_field)

def select_languages(api_key):
    translator = deepl.Translator(api_key)
    try:
        languages = [lang.code for lang in translator.get_source_languages()]
    except deepl.exceptions.AuthorizationException:
        QMessageBox.warning(mw, "Authorization Error", "Failed to retrieve languages. Please check your API key.")
        return None, None

    source_lang, ok = QInputDialog.getItem(mw, "Select Source Language", "Choose the source language:", languages, 0, False)
    if not ok or not source_lang:
        return None, None

    target_lang, ok = QInputDialog.getItem(mw, "Select Target Language", "Choose the target language:", languages, 0, False)
    if not ok or not target_lang:
        return None, None

    return source_lang, target_lang

def show_progress_dialog(total):
    progress_dialog = QProgressDialog("Translating notes...", "Break", 0, total, mw)
    progress_dialog.setWindowTitle("Translating")
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.setMinimumDuration(0)
    progress_dialog.forceShow()
    return progress_dialog

def update_progress(progress_dialog, current, total, start_time):
    elapsed_time = time.time() - start_time
    notes_remaining = total - current
    if current > 0:
        time_per_note = elapsed_time / current
        estimated_remaining_time = time_per_note * notes_remaining
    else:
        estimated_remaining_time = 0
    progress_dialog.setLabelText(f"Translated {current}/{total} notes\n"
                                 f"Remaining: {notes_remaining}\n"
                                 f"Estimated remaining time: {int(estimated_remaining_time)} seconds")
    progress_dialog.setValue(current)

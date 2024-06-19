import sys
import os
from aqt import mw
from aqt.qt import QInputDialog, QLineEdit, QMessageBox

# Ensure the lib path is added to sys.path
addon_path = os.path.dirname(__file__)
lib_path = os.path.join(addon_path, 'lib')
sys.path.insert(0, lib_path)

import deepl

# Function to get DeepL API key from the user
def get_api_key():
    while True:
        api_key, ok = QInputDialog.getText(mw, "DeepL API Key", "Enter your DeepL API key:", QLineEdit.EchoMode.Password)
        if not ok or not api_key:
            return ""
        else:
            try:
                translator = deepl.Translator(api_key)
                # Check if the API key is valid by fetching source languages
                translator.get_source_languages()
                return api_key
            except deepl.exceptions.AuthorizationException:
                QMessageBox.warning(mw, "Invalid API Key", "The API key you entered is invalid. Please try again.")

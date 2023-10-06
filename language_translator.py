import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QComboBox, QLabel, QSplitter, QHBoxLayout, QMessageBox
from googletrans import Translator, LANGUAGES

class LanguageTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Language Translator")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.splitter = QSplitter(self.central_widget)
        self.layout.addWidget(self.splitter)

        # Left side (source text and source language)
        self.left_widget = QWidget(self.splitter)
        self.left_layout = QVBoxLayout(self.left_widget)

        self.top_left_layout = QHBoxLayout()
        self.left_layout.addLayout(self.top_left_layout)

        self.source_language_combo = QComboBox(self.left_widget)
        self.source_language_combo.addItem("Auto Detect", "auto")
        for code, lang in LANGUAGES.items():
            self.source_language_combo.addItem(lang, code)
        self.top_left_layout.addWidget(QLabel("Source Language:", self.left_widget))
        self.top_left_layout.addWidget(self.source_language_combo)

        self.source_label = QLabel("Source Text:", self.left_widget)
        self.left_layout.addWidget(self.source_label)

        self.source_text_edit = QTextEdit(self.left_widget)
        self.source_text_edit.setPlaceholderText("Enter text to translate...")
        self.left_layout.addWidget(self.source_text_edit)

        # Right side (target text and target language)
        self.right_widget = QWidget(self.splitter)
        self.right_layout = QVBoxLayout(self.right_widget)

        self.top_right_layout = QHBoxLayout()
        self.right_layout.addLayout(self.top_right_layout)

        self.target_language_combo = QComboBox(self.right_widget)
        self.target_language_combo.addItem("Select Target Language", "")
        for code, lang in LANGUAGES.items():
            self.target_language_combo.addItem(lang, code)
        self.top_right_layout.addWidget(QLabel("Target Language:", self.right_widget))
        self.top_right_layout.addWidget(self.target_language_combo)

        self.target_label = QLabel("Translation:", self.right_widget)
        self.right_layout.addWidget(self.target_label)

        self.target_text_edit = QTextEdit(self.right_widget)
        self.target_text_edit.setReadOnly(True)
        self.right_layout.addWidget(self.target_text_edit)

        self.layout.addWidget(self.splitter)

        # Top buttons (Translate and Copy)
        self.top_buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.top_buttons_layout)

        self.translate_button = QPushButton("Translate", self.central_widget)
        self.translate_button.clicked.connect(self.translate_text)
        self.top_buttons_layout.addWidget(self.translate_button)

        self.copy_button = QPushButton("Copy Translation", self.central_widget)
        self.copy_button.clicked.connect(self.copy_translation)
        self.copy_button.setEnabled(False)
        self.top_buttons_layout.addWidget(self.copy_button)

        # Apply a custom stylesheet
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f4f4f4;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                font-size: 14px;
                padding: 4px;
            }
            QTextEdit {
                font-size: 14px;
                padding: 4px;
            }
        ''')

    def translate_text(self):
        source_text = self.source_text_edit.toPlainText()
        source_language_code = self.source_language_combo.currentData()
        target_language_code = self.target_language_combo.currentData()

        if not source_text:
            QMessageBox.information(self, "Info", "There is nothing to translate.")
        elif not target_language_code:
            QMessageBox.warning(self, "Warning", "Please select a target language.")
        else:
            translator = Translator()
            if source_language_code == "auto":
                translation = translator.translate(source_text, dest=target_language_code)
            else:
                translation = translator.translate(source_text, src=source_language_code, dest=target_language_code)
            self.target_text_edit.setPlainText(translation.text)
            self.copy_button.setEnabled(True)

    def copy_translation(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.target_text_edit.toPlainText())
        QMessageBox.information(self, "Info", "Translation copied to clipboard.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator_app = LanguageTranslatorApp()
    translator_app.show()
    sys.exit(app.exec())

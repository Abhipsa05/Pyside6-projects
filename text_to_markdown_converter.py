import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QSplitter, QHBoxLayout
from PySide6.QtGui import QTextOption
from PySide6.QtGui import QTextOption, QFont, QColor, QPalette
from mistune import Markdown

class WordWrapTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWordWrapMode(QTextOption.WordWrap)
        self.setFont(QFont("Segoe UI", 14))

class MarkdownPreviewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Markdown Previewer")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Left side: Editing area
        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)

        label_edit = QLabel("Markdown Editor")
        label_edit.setFont(QFont("Segoe UI", 16, QFont.Bold))
        left_layout.addWidget(label_edit)

        self.text_edit = WordWrapTextEdit(self)
        left_layout.addWidget(self.text_edit)

        self.preview_button = QPushButton("Convert to Markdown", self)
        self.preview_button.setFont(QFont("Segoe UI", 14))
        self.preview_button.setStyleSheet("background-color: #4CAF50; color: white;")
        left_layout.addWidget(self.preview_button)

        left_panel.setLayout(left_layout)

        # Right side: Preview area
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)

        label_preview = QLabel("Markdown Preview")
        label_preview.setFont(QFont("Segoe UI", 16, QFont.Bold))
        right_layout.addWidget(label_preview)

        self.preview_area = QTextEdit(self)
        self.preview_area.setReadOnly(True)
        self.preview_area.setWordWrapMode(QTextOption.WordWrap)
        self.preview_area.setFont(QFont("Segoe UI",14))
        right_layout.addWidget(self.preview_area)

        right_panel.setLayout(right_layout)

        # Create a splitter to adjust the size of editing and preview areas
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        layout.addWidget(splitter)

        self.md = Markdown()

        # Connect the "Convert to Markdown" button click event
        self.preview_button.clicked.connect(self.update_preview)

    def update_preview(self):
        input_text = self.text_edit.toPlainText()

        # Convert the input text to Markdown using mistune
        markdown_text = self.md(input_text)

        # Display the Markdown content in the preview area
        self.preview_area.setHtml(markdown_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownPreviewer()

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

    window.show()
    sys.exit(app.exec_())

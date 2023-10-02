import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QFont, QTextOption, QTextDocument
from PySide6.QtCore import Qt

class StickyNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sticky Note App")
        self.setGeometry(100, 100, 300, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_task_button)

        self.add_task_button.setStyleSheet(
            "background-color: #3CB371; color: white;"  # Green background, white text
        )

        # Apply dark theme to the Sticky Note App
        self.setStyleSheet(
            "background-color: #333333; color: white;"  # Dark background, white text
        )

        self.task_windows = []

    def add_task(self):
        task_text = self.text_edit.toPlainText().strip()
        if task_text:
            sticky_note = StickyNoteWindow(task_text)
            sticky_note.show()
            self.task_windows.append(sticky_note)
            self.text_edit.clear()

class StickyNoteWindow(QWidget):
    def __init__(self, task_text):
        super().__init__()

        self.setWindowTitle("Sticky Note")
        self.setFixedWidth(200)  # Fixed width

        self.layout = QVBoxLayout(self)

        # Styling for the sticky note
        self.setStyleSheet(
            "background-color: #fffbcc;"  # Light yellow background
            "border-radius: 10px;"  # Rounded corners
        )

        self.task_label = QLabel(self)
        self.task_label.setFont(QFont("Roboto", 12))
        self.task_label.setAlignment(Qt.AlignCenter)  # Align text in the center
        self.task_label.setWordWrap(True)
        self.task_label.setText(task_text)
        self.layout.addWidget(self.task_label)

        # Calculate the height of the text using QTextDocument
        doc = QTextDocument()
        doc.setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignLeft))
        doc.setPlainText(task_text)
        doc.setTextWidth(self.task_label.width())
        text_height = doc.size().height()

        # Adjust the height based on the text content
        if text_height > 150:  # Set a maximum height for the sticky note
            self.setFixedHeight(150)
        else:
            self.setFixedHeight(text_height + 50)  # Adjust height to fit the text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sticky_note = StickyNoteApp()
    sticky_note.show()
    sys.exit(app.exec())

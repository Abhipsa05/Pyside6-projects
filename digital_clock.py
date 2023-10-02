import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import QTimer, Qt, QTime
from PySide6.QtGui import QFont, QColor, QPalette

class DigitalClock(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Clock")
        self.setGeometry(100, 100, 400, 150)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.horizontal_layout.setAlignment(Qt.AlignCenter)

        self.vertical_layout = QVBoxLayout()  

        self.label = QLabel(self)
        self.vertical_layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every 1 second

        self.theme = "light"  # Default theme

        self.update_time()  # Initial update

        self.toggle_button = QPushButton("Toggle Theme", self)
        self.toggle_button.clicked.connect(self.toggle_theme)
        self.vertical_layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.set_light_theme()

        self.horizontal_layout.addLayout(self.vertical_layout) 

    def toggle_theme(self):
        if self.theme == "light":
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_light_theme(self):
        self.setStyleSheet("background-color: white;")

        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(0, 0, 255)) 
        self.label.setPalette(palette)

        self.label.setFont(QFont("Roboto", 40))  # Increase font size

        self.toggle_button.setStyleSheet(
            "background-color: lightgray; color: black;"
        )

        self.theme = "light"

    def set_dark_theme(self):
        self.setStyleSheet("background-color: black;")

        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0)) 
        self.label.setPalette(palette)

        self.label.setFont(QFont("Roboto", 40))  # Increase font size

        self.toggle_button.setStyleSheet(
            "background-color: black; color: white;"
        )

        self.theme = "dark"

    def update_time(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString("hh:mm:ss")
        self.label.setText(time_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec())

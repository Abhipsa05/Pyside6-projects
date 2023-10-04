import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QTextEdit, QLabel, QPushButton, QDialog, QVBoxLayout as DialogVBoxLayout, QMessageBox, QTimeEdit
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont

class ReminderDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Reminder")
        self.setGeometry(100, 100, 400, 200)

        self.layout = DialogVBoxLayout(self)

        self.reminder_text_edit = QTextEdit(self)
        self.layout.addWidget(self.reminder_text_edit)

        self.from_time_edit = QTimeEdit(self)
        self.from_time_edit.setDisplayFormat("HH:mm")
        self.layout.addWidget(self.from_time_edit)

        self.to_time_edit = QTimeEdit(self)
        self.to_time_edit.setDisplayFormat("HH:mm")
        self.layout.addWidget(self.to_time_edit)

        self.save_button = QPushButton("Save Reminder", self)
        self.save_button.clicked.connect(self.save_reminder)
        self.layout.addWidget(self.save_button)

    def save_reminder(self):
        reminder_text = self.reminder_text_edit.toPlainText()
        from_time = self.from_time_edit.time()
        to_time = self.to_time_edit.time()
        if reminder_text:
            self.accept()
            self.reminder = {
                "text": reminder_text,
                "from_time": from_time,
                "to_time": to_time,
            }
        else:
            QMessageBox.critical(self, "Error", "Reminder text cannot be empty!")

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calendar App")
        self.setFixedSize(400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.calendar_widget = QCalendarWidget(self)
        self.layout.addWidget(self.calendar_widget)
        self.calendar_widget.clicked.connect(self.show_reminder)
        self.calendar_widget.activated.connect(self.show_dialog_to_add_reminder)

        header = self.calendar_widget.findChild(QLabel, "qt_calendar_navigationbar")
        if header:
            header.setFont(QFont("Arial", 16))  
            header.setMinimumHeight(60)

        self.reminder_text = QTextEdit(self)
        self.reminder_text.setReadOnly(True)  
        self.layout.addWidget(self.reminder_text)

        self.current_date_label = QLabel(self)
        self.layout.addWidget(self.current_date_label)

        self.calendar_widget.setSelectedDate(QDate.currentDate())
        self.update_current_date_label()

        self.reminders = {}
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QCalendarWidget {
                background-color: white;
            }
            QTextEdit {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QCalendarWidget QTableView:selected {
                border: 2px solid red;  
            }
        """)

    def show_reminder(self):
        selected_date = self.calendar_widget.selectedDate()
        reminder_date_str = selected_date.toString("yyyy-MM-dd")

        if reminder_date_str in self.reminders:
            reminders_for_date = self.reminders[reminder_date_str]
            reminder_text = ""
            for reminder in reminders_for_date:
                reminder_text += f"{reminder['from_time'].toString('HH:mm')} - {reminder['to_time'].toString('HH:mm')}: {reminder['text']}\n"
            self.reminder_text.setPlainText(reminder_text)
        else:
            self.reminder_text.setPlainText("")

    def show_dialog_to_add_reminder(self):
        selected_date = self.calendar_widget.selectedDate()
        reminder_date_str = selected_date.toString("yyyy-MM-dd")

        dialog = ReminderDialog()

        if dialog.exec() == QDialog.Accepted:
            self.reminder_text.setPlainText("") 

            reminder = dialog.reminder
            if reminder:
                if reminder_date_str not in self.reminders:
                    self.reminders[reminder_date_str] = []
                self.reminders[reminder_date_str].append(reminder)

                QMessageBox.information(self, "Success", "Reminder saved for {}.".format(selected_date.toString("MMMM d, yyyy")))

            self.show_reminder()  

    def update_current_date_label(self):
        current_date = QDate.currentDate()
        self.current_date_label.setText("Today's Date: " + current_date.toString("MMMM d, yyyy"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calendar_app = CalendarApp()
    calendar_app.show()
    sys.exit(app.exec())
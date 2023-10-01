import sys
import requests
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLineEdit, QLabel, QTextBrowser
from PySide6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Currency Converter")
        self.setGeometry(100, 100, 400, 200)

        self.base_currency = "USD"
        self.api_key = "0b9db07bbd1d44d350192f2a"
        self.currencies = []

        self.initUI()
        self.load_currencies()
        self.fetch_exchange_rates()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_exchange_rates)
        self.timer.start(60000)  # Update rates every minute

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        font = QFont()
        font.setPointSize(12)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #333;
            }
            QLabel {
                font-size: 14px;
                color: #fff;
            }
            QLineEdit, QComboBox {
                font-size: 14px;
                background-color: #444;
                color: #fff;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QTextEdit {
                font-size: 14px;
                background-color: #222;
                color: #00FF00;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 5px;
            }
            QTextBrowser {
                font-size: 14px;
                background-color: #222;
                color: #00FF00;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.amount_label = QLabel("Amount:")
        layout.addWidget(self.amount_label)

        self.amount_input = QLineEdit(self)
        self.amount_input.textChanged.connect(self.convert_currency)
        layout.addWidget(self.amount_input)

        self.from_currency_label = QLabel("From Currency:")
        layout.addWidget(self.from_currency_label)

        self.from_currency_combo = QComboBox(self)
        self.from_currency_combo.currentTextChanged.connect(self.convert_currency)
        layout.addWidget(self.from_currency_combo)

        self.to_currency_label = QLabel("To Currency:")
        layout.addWidget(self.to_currency_label)

        self.to_currency_combo = QComboBox(self)
        self.to_currency_combo.currentTextChanged.connect(self.convert_currency)
        layout.addWidget(self.to_currency_combo)

        self.result_label = QLabel("Result:", self)
        self.result_label.setFont(font)
        layout.addWidget(self.result_label)

        self.result_display = QTextBrowser(self)
        self.result_display.setFont(font)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

    def load_currencies(self):
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/USD"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.currencies = list(data.get("conversion_rates", {}).keys())
            self.currencies.append(self.base_currency)
            self.currencies.sort()
            self.from_currency_combo.addItems(self.currencies)
            self.to_currency_combo.addItems(self.currencies)

    def fetch_exchange_rates(self):
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/USD"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.exchange_rates = data.get("conversion_rates", {})

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_currency_combo.currentText()
            to_currency = self.to_currency_combo.currentText()
            if from_currency != to_currency:
                conversion_rate = self.exchange_rates[to_currency] / self.exchange_rates[from_currency]
                result = amount * conversion_rate
                self.result_display.setText(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")

                cursor = self.result_display.textCursor()
                format = QTextCharFormat()
                format.setForeground(QColor("#00FF00"))  # Green color for highlighting
                cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
                cursor.setCharFormat(format)
            else:
                self.result_display.setText("No conversion needed")
        except ValueError:
            self.result_display.setText("Enter a valid amount")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec())

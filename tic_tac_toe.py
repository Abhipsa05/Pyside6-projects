import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtGui import QFont

class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tic-Tac-Toe")
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet("background-color: #333;")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #333;")

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_board_ui()

        self.status_label = QLabel("Player X's turn", self)
        self.status_label.setStyleSheet("color: #fff; font-size: 18px;")
        self.layout.addWidget(self.status_label, 3, 0, 1, 3)

    def create_board_ui(self):
        font = QFont()
        font.setPixelSize(24)

        for row in range(3):
            for col in range(3):
                button = QPushButton("", self)
                button.setFixedSize(100, 100)
                button.setFont(font)
                button.clicked.connect(lambda row=row, col=col: self.button_clicked(row, col))
                self.layout.addWidget(button, row, col)
                self.buttons[row][col] = button
                button.setStyleSheet(
                    "background-color: #fff; color: #333; border: 2px solid #333;"
                )

    def button_clicked(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            self.buttons[row][col].setEnabled(False)
            if self.check_winner(row, col):
                self.show_winner_message()
            elif self.check_board_full():  # Check for a tie after each move
                self.show_tie_message()
            else:
                self.toggle_player()

    def toggle_player(self):
        self.current_player = "X" if self.current_player == "O" else "O"
        self.status_label.setText(f"Player {self.current_player}'s turn")

    def check_winner(self, row, col):
        if (
            self.check_row(row) or
            self.check_column(col) or
            self.check_diagonal() or
            self.check_reverse_diagonal()
        ):
            return True
        return False
    
    def check_board_full(self):
        return all(all(cell != "" for cell in row) for row in self.board)

    def new_game(self):
        if self.game_over:  # Check if the game is over
            self.current_player = "X"
            self.board = [["" for _ in range(3)] for _ in range(3)]
            for row in self.buttons:
                for button in row:
                    button.setText("")
                    button.setEnabled(True)
            self.status_label.setText("Player X's turn")
            self.game_over = False  # Reset the game over flag

    def show_tie_message(self):
        tie_message = "It's a Tie! No one wins."
        msg_box = QMessageBox(self)
        msg_box.setText(tie_message)
        msg_box.setWindowTitle("Game Over")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.new_game)
        msg_box.setStyleSheet(
            "background-color: #333; color: #fff; font-size: 16px;"
        )
        msg_box.exec()
        self.game_over = True

    def check_row(self, row):
        return all(self.board[row][col] == self.current_player for col in range(3))

    def check_column(self, col):
        return all(self.board[row][col] == self.current_player for row in range(3))

    def check_diagonal(self):
        return all(self.board[i][i] == self.current_player for i in range(3))

    def check_reverse_diagonal(self):
        return all(self.board[i][2 - i] == self.current_player for i in range(3))

    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def show_winner_message(self):
        winner_message = f"Player {self.current_player} wins!"
        msg_box = QMessageBox(self)
        msg_box.setText(winner_message)
        msg_box.setWindowTitle("Game Over")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(
            "background-color: #333; color: #fff; font-size: 16px;"
        )
        msg_box.buttonClicked.connect(self.new_game)
        msg_box.exec()

    def new_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setEnabled(True)
        self.status_label.setText("Player X's turn")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec())

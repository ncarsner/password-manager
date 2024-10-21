from PyQt5 import QtWidgets, uic
from database import Database
from encryption import encrypt, decrypt


class PasswordManagerGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(PasswordManagerGUI, self).__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager")
        self.login_screen()

    def login_screen(self):
        self.login_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.login_widget)
        layout = QtWidgets.QVBoxLayout()

        self.master_password_label = QtWidgets.QLabel("Enter Master Password:")
        self.master_password_input = QtWidgets.QLineEdit()
        self.master_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button.clicked.connect(self.verify_master_password)

        layout.addWidget(self.master_password_label)
        layout.addWidget(self.master_password_input)
        layout.addWidget(self.login_button)
        self.login_widget.setLayout(layout)

    def verify_master_password(self):
        # Implement master password verification
        self.main_screen()

    def main_screen(self):
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QtWidgets.QVBoxLayout()

        self.add_password_button = QtWidgets.QPushButton("Add Password")
        self.add_password_button.clicked.connect(self.add_password)
        self.view_passwords_button = QtWidgets.QPushButton("View Passwords")
        self.view_passwords_button.clicked.connect(self.view_passwords)
        self.generate_password_button = QtWidgets.QPushButton("Generate Password")
        self.generate_password_button.clicked.connect(self.generate_password)

        layout.addWidget(self.add_password_button)
        layout.addWidget(self.view_passwords_button)
        layout.addWidget(self.generate_password_button)
        self.main_widget.setLayout(layout)

    def add_password(self):
        # Implement add password functionality
        pass

    def view_passwords(self):
        # Implement view passwords functionality
        pass

    def generate_password(self):
        # Implement password generation functionality
        pass


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     window = PasswordManagerGUI()
#     window.show()
#     app.exec_()

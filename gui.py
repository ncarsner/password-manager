import random
import string
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
        self.resize(900, 500)

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
        main_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        self.add_password_button = QtWidgets.QPushButton("Add Password")
        self.add_password_button.clicked.connect(self.add_password)
        self.view_passwords_button = QtWidgets.QPushButton("View Passwords")
        self.view_passwords_button.clicked.connect(self.view_passwords)
        self.generate_password_button = QtWidgets.QPushButton("Generate Password")
        self.generate_password_button.clicked.connect(self.generate_password)

        button_layout.addWidget(self.add_password_button)
        button_layout.addWidget(self.view_passwords_button)
        button_layout.addWidget(self.generate_password_button)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()  # Add stretch to push buttons to the top
        self.main_widget.setLayout(main_layout)

    def add_password(self):
        self.add_password_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.add_password_widget)
        layout = QtWidgets.QVBoxLayout()

        self.website_label = QtWidgets.QLabel("Website:")
        self.website_input = QtWidgets.QLineEdit()
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_input = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_password)

        layout.addWidget(self.website_label)
        layout.addWidget(self.website_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_button)
        self.add_password_widget.setLayout(layout)

    def save_password(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        encrypted_password = encrypt(password)
        self.db.add_password(website, username, encrypted_password, "")
        QtWidgets.QMessageBox.information(
            self, "Success", "Password saved successfully!"
        )
        self.main_screen()

    def view_passwords(self):
        self.view_passwords_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.view_passwords_widget)
        layout = QtWidgets.QVBoxLayout()

        self.passwords_table = QtWidgets.QTableWidget()
        self.passwords_table.setColumnCount(4)
        self.passwords_table.setHorizontalHeaderLabels(
            ["Website", "Username", "Password", "Notes"]
        )
        self.load_passwords()

        layout.addWidget(self.passwords_table)
        self.view_passwords_widget.setLayout(layout)

    def load_passwords(self):
        passwords = self.db.get_passwords()
        self.passwords_table.setRowCount(len(passwords))
        for row, password_data in enumerate(passwords):
            website, username, encrypted_password, notes = password_data[:4]
            decrypted_password = decrypt(encrypted_password)
            self.passwords_table.setItem(row, 0, QtWidgets.QTableWidgetItem(website))
            self.passwords_table.setItem(row, 1, QtWidgets.QTableWidgetItem(username))
            self.passwords_table.setItem(
                row, 2, QtWidgets.QTableWidgetItem(decrypted_password)
            )
            self.passwords_table.setItem(row, 3, QtWidgets.QTableWidgetItem(notes))

    def generate_password(self):
        length = random.randint(8, 20)
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(characters) for _ in range(length))

        self.generated_password_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.generated_password_widget)
        layout = QtWidgets.QVBoxLayout()

        self.generated_password_label = QtWidgets.QLabel("Generated Password:")
        self.generated_password_display = QtWidgets.QLineEdit(password)
        self.generated_password_display.setReadOnly(True)
        self.copy_button = QtWidgets.QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        layout.addWidget(self.generated_password_label)
        layout.addWidget(self.generated_password_display)
        layout.addWidget(self.copy_button)
        self.generated_password_widget.setLayout(layout)

    def copy_to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.generated_password_display.text())
        QtWidgets.QMessageBox.information(
            self, "Copied", "Password copied to clipboard!"
        )


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     window = PasswordManagerGUI()
#     window.show()
#     app.exec_()

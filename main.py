from gui import PasswordManagerGUI
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PasswordManagerGUI()
    window.show()
    app.exec_()

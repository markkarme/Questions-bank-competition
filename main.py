from PyQt5 import QtWidgets,QtCore
from view_manager import BankQuestion
def __Test__():
    app = QtWidgets.QApplication([])
    m = BankQuestion()
    m.show()
    app.exec_()
if __name__ == "__main__":
    __Test__()
    
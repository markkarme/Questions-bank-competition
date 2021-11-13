from PyQt5 import QtWidgets,QtCore,QtGui, sip
from views import true_view
from PyQt5.QtWidgets import QGraphicsDropShadowEffect,QSizeGrip
from PyQt5.QtCore import Qt,QPropertyAnimation,QStringListModel
class TrueWidget(true_view.Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

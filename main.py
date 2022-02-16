import base64
import os
import os.path
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

def PRGA(S):
    P = str(input("Input P: "))
    i = 0
    j = 0
    for idx in range (len(P)-1):
        i = (i+1)%256
        j = (j+S[i])%256
        S[i], S[j] = S[j], S[i]
        t = (S[i]+S[j])%256
        u = S[t] #keystream
    return u
        # c = u^P[idx]

class Landing(QDialog):
    def __init__(self):
        super(Landing, self).__init__()
        loadUi('landingpage.ui', self)
        # self.vigButton.clicked.connect(self.gotoVig)

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(Landing())  # Index jadi 0   
widget.setCurrentIndex(0)
widget.setFixedWidth(780)
widget.setFixedHeight(319)
widget.show()
app.exec_()
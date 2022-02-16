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
        self.teksButton.clicked.connect(self.gotoText)
        self.uploadButton.clicked.connect(self.gotoUpload)
    def gotoText(self):
        widget.setCurrentIndex(2)
    def gotoUpload(self):
        widget.setCurrentIndex(1)
class Text(QDialog):
    def __init__(self):
        super(Text, self).__init__()
        loadUi('text.ui', self)
        self.encryptB.clicked.connect(self.encrypt)
        self.decryptB.clicked.connect(self.decrypt)
        self.uploadedFile = None 
    def encrypt(self): 
        kunci = self.kunci.text()
        teks = self.teks.text() 
        self.hasil.setText('keluaran')   
    def decrypt(self):    
        kunci = self.kunci.text()
        teks = self.teks.text() 
        self.hasil.setText('keluaranx')   
class Upload(QDialog):
    def __init__(self):
        super(Upload, self).__init__()
        loadUi('upload.ui', self)
        self.uploadButton.clicked.connect(self.upload)
        self.encryptB.clicked.connect(self.encrypt)
        self.decryptB.clicked.connect(self.decrypt)
        self.uploadedFile = None 
    def encrypt(self): 
        kunci = self.kunci.text()
        self.hasil.setText('keluaran')   
    def decrypt(self):    
        kunci = self.kunci.text()
        self.hasil.setText('keluaranx')   
    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Upload CV File", "")
        if fileName:
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
        else:
            print("No file selected")  
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(Landing())  # Index jadi 0  
widget.addWidget(Upload())  # Index jadi 1 
widget.addWidget(Text())  # Index jadi 2
widget.setCurrentIndex(0)
widget.setFixedWidth(780)
widget.setFixedHeight(319)
widget.show()
app.exec_()
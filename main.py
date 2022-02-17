import base64
import os
import os.path
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import codecs


def shortenKey(key): #memendekkan panjang key menjadi 256 bit
    temp_key = list(key)
    new_key = []
    for i in range(32):
        new_key.append(temp_key[i])
    return new_key

def ksa_lsfr(key):
    key_length = len(key)

    if(len(key)<=32):  #mengulang key jika panjang key kurang dari 256 bit
        key = list(key)
        for i in range(len(key)):
            key[i] = ord(key[i])
        for i in range(32 - len(key)): 
            key.append(key[i % len(key)])
    else: #memendekkan panjang key menjadi 256 bit
        shortenKey(key)

    #LSFR    
    lsfr = []
    biner = ''.join(format(i, '08b') for i in key)
    l = len(biner)
    for i in range(l):
        lsfr.append(biner[l-1])
        biner = str( int(biner[l-1]) ^ int(biner[0])) + biner[0:l-1]

    #KSA
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + int(lsfr[i]) + int((key[i % key_length]))) % 256
        S[i], S[j] = S[j], S[i] 

    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i+1)%256
        j = (j+S[i])%256
        S[i], S[j] = S[j], S[i]
        t = (S[i]+S[j])%256
        u = S[t] #keystream
        yield u
        # c = u^P[idx]

def convert(key, teks): # Encrypt & decrypt
    input = list()
    for c in teks :
        input.append(ord(c))
    keystream = PRGA(ksa_lsfr(key))

    result = []
    for i in input:
        r = ("%02X" % (i ^ next(keystream)))    
        result.append(r)
    output = ''.join(result)
    return (codecs.decode(output, 'hex_codec').decode('latin-1'))

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
        keluaran = convert(kunci,teks)
        keluaran = 'Hasil Enkripsi: ' + keluaran
        print(keluaran)
        self.hasil.setText(keluaran)   
    def decrypt(self):    
        kunci = self.kunci.text()
        teks = self.teks.text() 
        keluaran = convert(kunci,teks)
        keluaran = 'Hasil Dekripsi: ' + keluaran
        self.hasil.setText(keluaran)   
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
        keluaran = convert(kunci,data)
        keluaran = 'Hasil Enkripsi: ' + keluaran
        self.hasil.setText(keluaran)  
    def decrypt(self):    
        kunci = self.kunci.text()
        keluaran = convert(kunci,data)
        keluaran = 'Hasil Dekripsi: ' + keluaran
        self.hasil.setText(keluaran)   
    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Upload File", "")
        if fileName:
            global data
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            file1 = open(fileName, "rt")
            data = file1.read()
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
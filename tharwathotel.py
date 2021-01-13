from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import os
from os import path
import project2
import booking_before_edit
FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"hoteltrial.ui"))

class App_WindowHurghada(QMainWindow , FORM_CLASS):
    def __init__(self,STATUS_OF_USER,HotelName,UserName,parent=None):
        super(App_WindowHurghada,self).__init__(parent)
        QMainWindow. __init__(self)
        self.setupUi(self)
        self.Handle_Ui()
        self.Transation()
        self.userSTATUS=STATUS_OF_USER
        self.HotelName=HotelName
        self.UserName=UserName

    def Handle_Ui(self) :
        self.setWindowTitle('hurhghada hotel')

    def Transation(self):
        self.BookBtn.clicked.connect(self.open_Booking)
        self.pushButton_2.clicked.connect(self.Back_To_Main)

    def open_Booking(self):
        self.BookPageObj=booking_before_edit.MainBookingPage(self.userSTATUS,self.HotelName,self.UserName)
        self.BookPageObj.show()
        self.close()

    def Back_To_Main(Self):
        Self.IntroPageObj=project2.Intro_Main(Self.userSTATUS,Self.UserName)
        Self.IntroPageObj.show()
        Self.IntroPageObj.pushButton.setVisible(False)
        Self.IntroPageObj.pushButton_2.setVisible(False)
        
        Self.close()    

        
        
        
def main():
    app = QApplication(sys.argv)
    window = App_WindowHurghada(0,"","")
    window.show()
    app.exec_()
   
if __name__ == "__main__":
    main()
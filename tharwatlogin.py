from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import os
from os import path

import sqlite3
import SQLiteDB_Design

import index
from botros import *
import project2
from check_in import *


FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"login1.ui"))

class App_Window(QMainWindow , FORM_CLASS):
    def __init__(self,name,parent=None):
        super(App_Window,self).__init__(parent)
        QMainWindow. __init__(self)
        self.setupUi(self)
        self.Handle_Ui()
        self.Transition()
        self.LIconnect_DB()
        self.guestname=name

    def LIconnect_DB(self):
        self.conn=sqlite3.connect('projectDB.db')
        self.c=self.conn.cursor()

    def Handle_Ui(self) :
        self.setWindowTitle('LOGIN')

    def Transition(self):
        self.pushButton_2.clicked.connect(self.Open_Admin)
        self.pushButton_4.clicked.connect(self.open_Staff)
        self.pushButton.clicked.connect(self.open_Guest)
        self.pushButton_3.clicked.connect(self.Back)

    def Back(Self):
        Self.MainPageObject=project2.Intro_Main(0,"")
        Self.MainPageObject.SignBtn.setVisible(False)
        Self.MainPageObject.show()
        Self.close()  

    def open_Guest(self):
        EnteredUsername=self.lineEdit.text()
        EnteredPassword=self.lineEdit_2.text()
        query=(""" SELECT Password FROM GuestInfo WHERE Username = ?""" )
        queryforcheckinpage=("SELECT Booked FROM GuestInfo WHERE Username=?")

        self.c.execute(query,(EnteredUsername,))
        self.conn.commit()
        rightPass=self.c.fetchall()[0][0]
        self.c.execute(queryforcheckinpage,(EnteredUsername,))
        self.conn.commit()
        bookingstatus=self.c.fetchall()[0][0]

        if rightPass==EnteredPassword:
            if bookingstatus==1:
                self.checkinpageobj=Checkin_Main(bookingstatus,EnteredUsername)
                self.checkinpageobj.pushButton_8.setVisible(True)
                self.checkinpageobj.show()
                self.close()
            else:    
                statusQuery=("SELECT SignedStatus FROM GuestInfo WHERE Username=? AND Password=?")
                self.c.execute(statusQuery, (EnteredUsername,EnteredPassword))
                self.conn.commit()
                userstatus=self.c.fetchall()[0][0]
                self.browseObj=project2.Intro_Main(userstatus,EnteredUsername)
                if userstatus==1:
                    self.browseObj.pushButton.setVisible(False)
                    self.browseObj.pushButton_2.setVisible(False)
                self.browseObj.show()
                self.browseObj.SignBtn.setVisible(True)
                self.browseObj.SignBtn.setText(EnteredUsername)
                self.browseObj.SignBtn.setEnabled(False)            
                self.close()
        else:
            QMessageBox.warning(self,"Incorrect Password","Please enter the right password")
            self.lineEdit_2.setText("")    
        #print(rightPass)    



    def Open_Admin(self):
        if self.lineEdit_3.text()=="PureLifeAdmin" and self.lineEdit_4.text()=="PureLifeAdmin":
            self.obj=index.MainApp()
            self.obj.show()
            self.close()
            
        
    def open_Staff(self):
        staffUser=self.lineEdit_5.text()
        staffPass=self.lineEdit_6.text()
        query=("SELECT Password FROM EmployeeInfo WHERE Name =?")
        self.c.execute(query,(staffUser,))
        self.conn.commit()
        sure=self.c.fetchall()[0][0]
        if sure==staffPass:
            self.staffObj=Botros(staffUser)
            self.staffObj.show()
            self.close()
        else:
            QMessageBox.warning(self,"Incorrect Password","Please enter the right password")
            self.lineEdit_6.setText("")                         
        
        
def main():
    app = QApplication(sys.argv)
    window = App_Window("")
    window.show()
    app.exec_()
   
if __name__ == "__main__":
    main()
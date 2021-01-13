from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import datetime
import sqlite3
import SQLiteDB_Design
import project2

import sys

MainUI,_ = loadUiType('BOOKING.ui')

class MainBookingPage(QMainWindow , MainUI):
    def __init__(self,STATUSOFUSER,HotelName,UserName ,parent=None):
        super(MainBookingPage, self). __init__(parent)
        QMainWindow. __init__(self)
        self.setupUi(self)
        self.setWindowTitle("Pure life hotels")
        self.Transation()
        self.Booking_ConnectDB()
        self.showCostbtn.setCheckable(True)
        self.CostDisplay.setReadOnly(True)
        self.stateofuser=STATUSOFUSER
        self.HotelName=HotelName
        self.UserName=UserName
        #print(self.UserName)

    def Booking_ConnectDB(Self):
        Self.conn=sqlite3.connect('projectDB.db')
        Self.c=Self.conn.cursor()        

    def Transation(Self):
        Self.pushButton_6.clicked.connect(Self.Filling_Booking_Data)
        Self.pushButton.clicked.connect(Self.LogOut)
        Self.pushButton_5.clicked.connect(Self.Check_Booking_Request_Status)    
        
        
    def LogOut(Self):
        Self.MainPageObject=project2.Intro_Main(0,"")
        query=("UPDATE GuestInfo SET SignedStatus=? WHERE Username=?")
        entry=(0,Self.UserName)
        Self.c.execute(query,entry)
        Self.conn.commit()
        Self.MainPageObject.show()
        Self.close()         
        
    SignleRoomPerNight=600
    DoubleRoomPerNight=450
    FamilyRoomPerNight=350
    Total_Price=float(0)
    BookUsername=""
    BookPassword=""
    BookEmail=""
    BookMobile=""
    BookAddress=""
    BookNationalId=""
    BookGender=""
    RoomType=""
    AdultsNo=0
    KidsNo=0
    TaxiRequest=0
    checkInDateDay=0
    checkOutDateDay=0
    # pypalcardtype=""
    # pypalCardnumber=""
    # pypalCardtype=""
    # pypalExpirationdate=""
    # pypalSecuritycode=""
    # pycreditcardname=""
    # pycreditcardnumber=""
    # pycreditcardcvv=""
    # pycreditExpiredate=""
    # pycreditcountryside=""

    def Filling_Booking_Data(Self):
        # pypalcardtype=Self.lineEdit_21.text()
        # pypalCardnumber=Self.lineEdit_14.text()
        # pypalCardtype=Self.comboBox_3.currentText()
        # pypalExpirationdate=Self.lineEdit_15.text()
        # pypalSecuritycode=Self.lineEdit_15.text()
        # pycreditcardname=""
        # pycreditcardnumber=""
        # pycreditcardcvv=""
        # pycreditExpiredate=""
        # pycreditcountryside=""
        Self.BookUsername=Self.lineEdit_7.text()
        Self.BookPassword=Self.lineEdit_8.text()
        Self.BookEmail=Self.lineEdit_11.text()
        Self.BookMobile=Self.lineEdit_12.text()
        Self.BookAddress=Self.lineEdit_9.text()
        Self.BookNationalId=Self.lineEdit_10.text()
        if Self.radioButton_7.isChecked()==True:
            Self.BookGender='Male'
        elif Self.radioButton_3.isChecked()==True:
            Self.BookGender="Female"    
        Self.RoomType=Self.comboBox_2.currentText()
        Self.AdultsNo=Self.spinBox_4.value()
        Self.KidsNo=Self.spinBox_3.value()
        if Self.radioButton_9.isChecked()==True:
            Self.TaxiRequest=1
        elif Self.radioButton_8.isChecked()==True:
            Self.TaxiRequest=0
        checkInDate=Self.dateEdit_4.date()
        checkInDate=checkInDate.toString()
        checkInDate=checkInDate.split()
        checkInDay=checkInDate[0]
        Self.checkInDateDay=int(checkInDate[2])
        checkInDateMonth=checkInDate[1]
        checkInDateYear=checkInDate[3]
        checkOutDate=Self.dateEdit_3.date()
        checkOutDate=checkOutDate.toString()
        checkOutDate=checkOutDate.split()
        checkOutDay=checkOutDate[0]
        Self.checkOutDateDay=int(checkOutDate[2])
        checkOutDateMonth=checkOutDate[1]
        checkOutDateYear=checkOutDate[3]
        if Self.RoomType=='Single':
            Self.Total_Price=Self.Total_Price+(Self.SignleRoomPerNight*(Self.checkOutDateDay-Self.checkInDateDay+1))
        elif Self.RoomType=='Double':
            Self.Total_Price=Self.Total_Price+(Self.DoubleRoomPerNight*(Self.checkOutDateDay-Self.checkInDateDay+1))
        elif Self.RoomType=='Family':
            Self.Total_Price=Self.Total_Price+(Self.FamilyRoomPerNight*(Self.checkOutDateDay-Self.checkInDateDay+1))

        if Self.TaxiRequest==1:
            Self.Total_Price=Self.Total_Price+200
        #if Self.showCostbtn.isChecked():
        Self.CostDisplay.setText(str(Self.Total_Price))
        
        ## Now i will check if This User already Signed in or not to add to it the other data ##
        Self.c.execute("SELECT Username FROM GuestInfo")
        Self.conn.commit()        
        for Atuple in Self.c.fetchall():
            for Ausername in Atuple:
                if Self.BookUsername==Ausername:
                    newQuery=(""" UPDATE GuestInfo
                                    SET Mobile = ?,Address=?,NationalId=?,Gender=?,BasicCost=?,CheckInDay=?,CheckOutDay=?,
                                        CarRental=?,AdultsNo=?,KidsNo=?,RoomType=?,SignedStatus=?,Booked=?,Hotel=?
                                    WHERE Username=?  """)
                    Self.c.execute(newQuery,(Self.BookMobile,Self.BookAddress,Self.BookNationalId,Self.BookGender,Self.Total_Price,
                                              Self.checkInDateDay,Self.checkOutDateDay,Self.TaxiRequest,Self.AdultsNo,
                                              Self.KidsNo,Self.RoomType,Self.stateofuser,1,Self.HotelName,Self.BookUsername))
                    Self.conn.commit()


        anotherquery=("SELECT * FROM GuestInfo WHERE Username=?")
        Self.c.execute(anotherquery,(Self.BookUsername,))
        Self.conn.commit()
        for item in Self.c.fetchall():
            print(item)

    def Check_Booking_Request_Status(self):
        queryForStatus=(""" SELECT BlackListed, Booked From GuestInfo WHERE Username=? """)
        self.c.execute(queryForStatus,(self.UserName,))
        self.conn.commit()
        x=self.c.fetchall()
        BlackListed,Booked = [list(c) for c in zip(*x)]
        BlackListedIndicator=BlackListed[0]
        BookedIndicator=Booked[0]
        # BlackListedStatus=self.c.fetchall()[0][0]
        # BookedStatus=self.c.fetchall()[0][1]
        print(self.c.fetchall())
        if BookedIndicator==1:
            if BlackListedIndicator!=1:
                QMessageBox.about(self,"Your Booking Request Status","Your Booking Request is confirmed, Thank you !")
            else:
                query=("UPDATE GuestInfo SET Booked=? WHERE Username=?")
                entry=(0,Self.UserName)
                Self.c.execute(query,entry)
                Self.conn.commit()
                QMessageBox.about(self,"Your Booking Request Status","we sorry to be late, you will know soon the status of your booking request, Have a nice day!")
        else:
            QMessageBox.about(self,"Your Booking Request Status","sorry but you are not booked yet!")




    

        #Self.listView.addItem(Total_Price)
   

    # def get_Cost(Self):
    #     print(Self.Total_Price)    

    





def main():
    app = QApplication(sys.argv)
    window = MainBookingPage(0,"","")
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

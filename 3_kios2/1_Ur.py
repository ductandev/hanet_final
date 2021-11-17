from datetime import datetime, timedelta, timezone
import time
import random
import os
from time import sleep

import threading

from serial import Serial
from paho.mqtt import client as mqtt_client

from csv import DictWriter
from json import dumps, load, loads

from GUIVIDEO import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication,QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import  QThread,  pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineSettings


broker = '192.168.51.104'
port = 1883
# topic = "/topic/detected/C21025B546"
topic = "/topic/detected/C21282M528"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'lam'
password = '1234'

f = open('hrdata/data/data5.json')
data = load(f)

f1 = open('hrdata/data/data3.json')
infor_s = load(f1)

# address_congty = "38 Quang Trung, Hiệp Phú, Quận 9, Thành phố Hồ Chí Minh"

def getNameStudent(id):
    for i in data:
        if id == str(i['maNV']):
            name = i['tenNV']
            return name
    return None

def getClassStudent(id):
    for i in data:
        if id == str(i['maNV']):
            class_student = i['chucVu']
            return class_student
    return None


def getIDStudent(id):
    for i in data:
        if id == str(i['maNV']):
            id_student = i["maNV"]
            return str(id_student)
    return None


# Mapping data among  hanet data and  titkul data
def mapping_data(id):
    for i in infor_s:
        if str(id) == i['personID']:
            return str(i['aliasID'])
    return None



class Thread(QThread):
    changeName = pyqtSignal(str, name='name')
    changeMnv = pyqtSignal(str, name='mnv')
    changeTime = pyqtSignal(str, name='time')
    changePosition = pyqtSignal(str, name='position')
    pictureID = pyqtSignal(QImage, name='avatarID')
    changeTemperature = pyqtSignal(str, name='temperature')
    arduino = Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

    def read_distance(self):
        data = self.arduino.readline()
        return data

    def write_read(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        sleep(0.05)
        data = self.arduino.readline()
        return data

    def upload_info(self, staffMnv, data_time, temperature):
        with open ("hrdata/data/recognization.csv", mode = "+a") as re_csv_file:
            fieldnames = ['ID', 'Date' , 'Temperature']
            writer = DictWriter(re_csv_file, fieldnames=fieldnames)
            writer.writerow({'ID': str(staffMnv), 'Date': str(data_time), 'Temperature': temperature})
        with open ("hrdata/data/recognizationbakup.csv", mode = "+a") as re_csv_file1:
            fieldnames = ['ID', 'Date' , 'Temperature']
            writer = DictWriter(re_csv_file1, fieldnames=fieldnames)
            writer.writerow({'ID': str(staffMnv), 'Date': str(data_time), 'Temperature': temperature}) 

    def soud_warning(self, staffName):
        os.system("mpg123 amthanh/warning.mp3")

    def soud_succc(self, staffName):
        os.system("mpg123 amthanh/thanhcong_VT.mp3")

    def soud_sunkonown(self, staffName):
        os.system("mpg123 amthanh/nguoila_VT.mp3")

    def check_temp(self, staffName):
        os.system("mpg123 amthanh/Noti_nhiet_VT.mp3")

    def Nhietdo(self, xyss):

        while True:
            try:
                if time.time() - self.start_guiIcon  > 10:
                    self.start_guiIcon = time.time() 
                    photoID = QImage('Image/3.png')
                    self.pictureID.emit(photoID)
                    self.changeName.emit(str(""))
                    self.changeMnv.emit(str(""))
                    self.changePosition.emit(str(""))
                    self.changeTime.emit(str(""))
                    break
            except Exception as e:
                pass

    def UI_info(self, id_name1, times_id):
        self.temperature = round(random.uniform(36.5,37.2),2)
        while True:
            try:
                # num = '?'
                # value = self.write_read(num).decode("utf8","ignore").split("$")
                # x_max = float(value[0])
                self.temperature = round(random.uniform(36.5,37.2),2)#round(0.1455*float(x_max) + 32.108,2)  
                if (self.temperature > 37.5):
                    if (self.temperature > 38.5):
                        self.temperature= 38.5 
                    t1_warning = threading.Thread(target=self.soud_warning, args=( "W", ))
                    t1_warning.start() 
                    infor_s_up_1 = threading.Thread(target=self.upload_info, args=(self.id_name , self.sec, str(self.temperature)))
                    infor_s_up_1.start() 
                    self.changeTemperature.emit(str(self.temperature))
                if (self.temperature < 35.5):
                    self.temperature= 35.5 
                self.changeTemperature.emit(str(self.temperature))
                break

            except Exception as e:
                print("ajkdshajkfdkjsaggdkjagkjdgakj", e)
                try:
                    arduino = Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
                except Exception as e:
                    print(e)
                break
        try:
            if id_name1 != "None":
                self.start_guiIcon = time.time()
                self.staffName = getNameStudent(self.id_name)
                self.position = getClassStudent(self.id_name)
                self.staffMnv = getIDStudent(self.id_name)
                self.changeName.emit(str(self.staffName))
                self.changeMnv.emit(str(self.staffMnv))
                self.changePosition.emit(str(self.position)) 
                self.changeTime.emit(str(times_id.strftime("%H:%M:%S")))
                photoID = QImage('imageskios/{}/{}.png'.format(str(self.id_name), str(self.id_name)))
                self.pictureID.emit(photoID)
                if str(self.temperature) != "None":
                    if float(self.temperature) < 37.5:
                        soud_s0 = threading.Thread(target=self.soud_succc, args=("W", ))
                        soud_s0.start()
                self.changeTemperature.emit(str(self.temperature))
                infor_s_up = threading.Thread(target=self.upload_info, args=(self.id_name , times_id, str(self.temperature)))
                infor_s_up.start()            
            else:
                self.start_guiIcon = time.time()
                self.id_name = "None"
                self.changeName.emit(str("Người Lạ "))
                self.changeMnv.emit(str("?"))
                self.changePosition.emit(str("?"))
                self.changeTime.emit(str(times_id.strftime("%H:%M:%S")))
                photoID = QImage('Image/nguoila.png')
                self.pictureID.emit(photoID)
                self.changeTemperature.emit(str(self.temperature))
            infor_s_nhiet = threading.Thread(target=self.Nhietdo, args=("A",))
            infor_s_nhiet.start() 
        except Exception as e:
            self.changeName.emit(str("Người Lạ "))
            self.changeMnv.emit(str("?"))
            self.changePosition.emit(str("?"))
            self.changeTime.emit(str(times_id.strftime("%H:%M:%S")))
            photoID = QImage('Image/nguoila.png')
            self.pictureID.emit(photoID)
            self.changeTemperature.emit(str(self.temperature))
            print(e)
        

    def on_message(self, client, userdata, msg):
        try:
            s = loads(msg.payload.decode())
            self.personID = s['person_id']
            self.personType = s['person_type']
            self.personTime = s['date_time']
            self.sec = datetime.fromtimestamp(int(self.personTime), timezone(timedelta(hours=7)))
            self.start_guiIcon = time.time()
            if self.personType == 0:
                self.id_name = mapping_data(self.personID)
                self.UI_info(self.id_name , self.sec)
            elif self.personType == 2:
                soud_s2 = threading.Thread(target=self.soud_sunkonown, args=(self.personID, ))
                soud_s2.start()
                self.UI_info("None" , self.sec)
        except Exception as e:
            print(e)
            pass
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)
        return self.client

    def subscribe(self, client: mqtt_client):
        self.client.subscribe(topic)
        self.client.on_message = self.on_message


    def run(self):

        self.client = self.connect_mqtt()
        self.subscribe(self.client)
        self.client.loop_forever()


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.position = QtWidgets.QLabel(self.centralwidget)
        # self.address = QtWidgets.QLabel(self.centralwidget)
        self.temp = QtWidgets.QLabel(self.centralwidget)
        self.time_log = QtWidgets.QLabel(self.centralwidget)
        self.name_nv = QtWidgets.QLabel(self.centralwidget)
        self.mnv = QtWidgets.QLabel(self.centralwidget)
        self.photoID = QtWidgets.QLabel(self.centralwidget)
        self.logo_vietjean = QtWidgets.QLabel(self.centralwidget)
        self.welcome_vitajean = QtWidgets.QLabel(self.centralwidget)
        
        self.titkul_hotline = QtWidgets.QLabel(self.centralwidget)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layout1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        
        th = Thread(self.centralwidget)
        th.changeName.connect(lambda name: self.setName(name))
        th.changeMnv.connect(lambda mnv: self.setMnv(mnv))
        th.changePosition.connect(lambda position: self.setPosition(position))
        th.changeTime.connect(lambda time: self.setTime(time))
        th.pictureID.connect(lambda photoID: self.setPhotoID(photoID))
        th.changeTemperature.connect(lambda temp: self.setTemperature(temp))
        th.start()


    @pyqtSlot(QImage, name='avatarID')
    def setPhotoID(self, photoID):
        photoID = QPixmap.fromImage(photoID)
        self.photoID.setStyleSheet("background-color: none")        
        self.photoID.setPixmap(photoID)

    @pyqtSlot(str, name='time')
    def setTime(self, time):
        self.time_log.setText('Thời gian: ' + time)

    @pyqtSlot(str, name='temperature')
    def setTemperature(self, temperature):
        if temperature != "None":
            try:
                if (float(temperature) >= 37.5):
                    self.temp.setStyleSheet("background-color: red;  border: 1px solid black;")
                else:
                    self.temp.setStyleSheet("background-color: none;  border: 1px solid none;")
            except Exception as e:
                temperature = "None"
                self.temp.setStyleSheet("background-color: red;  border: 1px solid black;")
            self.temp.setText('Nhiệt độ: ' + temperature + '°C')
        else:
            self.temp.setText('Nhiệt độ: ' + temperature)

    @pyqtSlot(str, name='name')
    def setName(self, name):
        self.name_nv.setText('Họ và Tên: ' + name)

    @pyqtSlot(str, name='mnv')
    def setMnv(self, name):
        self.mnv.setText('Mã nhân viên: ' + name)

    @pyqtSlot(str, name='position')
    def setPosition(self, position):
        self.position.setText('Chức vụ: ' + position)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("background-color: white")
        MainWindow.resize(1080, 1920)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 1920))
        MainWindow.setSizeIncrement(QtCore.QSize(1080, 1920))
        MainWindow.setBaseSize(QtCore.QSize(1080, 1920))
        font = QtGui.QFont('Arial', 10)
        self.browser = window1()
        font.setPointSize(8)

        MainWindow.setFont(font)
        self.centralwidget.setObjectName("centralwidget")


        self.logo_vietjean.setGeometry(QtCore.QRect(0, 120, 1080, 169))
        self.logo_vietjean.setText("")
        self.logo_vietjean.setPixmap(QtGui.QPixmap("Image/2.png"))
        self.logo_vietjean.setScaledContents(True)
        self.logo_vietjean.setObjectName("logo_vietjean")

        self.welcome_vitajean.setGeometry(QtCore.QRect(0, 0, 1080, 119))
        self.welcome_vitajean.setText("")
        self.welcome_vitajean.setPixmap(QtGui.QPixmap("Image/1.png"))
        self.welcome_vitajean.setScaledContents(True)
        self.welcome_vitajean.stackUnder(self.logo_vietjean)
        self.welcome_vitajean.setObjectName("welcome_vitajean")

        self.photoID.setGeometry(QtCore.QRect(284, 300, 500, 500))
        self.photoID.setText("")
        # self.photoID.setPixmap(QtGui.QPixmap("Image/circled_user_male_480px_new.png"))
        self.photoID.setPixmap(QtGui.QPixmap("Image/3.png"))
        # self.photoID.setStyleSheet(" border: 10px solid #ff6b00; border-radius: 250px; ")
        self.photoID.setScaledContents(True)
        self.photoID.setObjectName("photoID")

        self.titkul_hotline.setGeometry(QtCore.QRect(0, 1782, 1080, 100))
        self.titkul_hotline.setText("")
        self.titkul_hotline.setPixmap(QtGui.QPixmap("Image/titkul_hotline3.png"))
        self.titkul_hotline.setScaledContents(True)
        self.titkul_hotline.setObjectName("titkul_hotline")

        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 1055, 1040, 720))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.web = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.web.setObjectName("web")
        
        self.layout1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setObjectName("layout1")
        self.layout1.addWidget(self.browser)

        self.name_nv.setGeometry(QtCore.QRect(220, 810, 800, 50))
        self.name_nv.setWordWrap(True)
        font = QtGui.QFont('Arial', 22)
        font.setBold(True)
        self.name_nv.setFont(font)
        self.name_nv.setStyleSheet("background-color: none;  border: 1px solid none;")

        self.position.setGeometry(QtCore.QRect(220, 850, 500, 50))
        font = QtGui.QFont('Arial', 20)
        # font.setItalic(True)
        self.position.setFont(font)
        self.position.setStyleSheet("background-color: none;  border: 1px solid none;")

        self.mnv.setGeometry(QtCore.QRect(220, 890, 500, 50))
        font = QtGui.QFont('Arial', 20)
        # font.setItalic(True)
        self.mnv.setFont(font)
        self.mnv.setStyleSheet("background-color: none;  border: 1px solid none;")

        self.time_log.setGeometry(QtCore.QRect(220, 930, 260, 50))
        font = QtGui.QFont('Arial', 20)
        self.time_log.setFont(font)
        self.time_log.setStyleSheet("background-color: none;  border: 1px solid none;")

        self.temp.setGeometry(QtCore.QRect(220, 970, 355, 50))
        font = QtGui.QFont('Arial', 20)
        self.temp.setFont(font)
        self.temp.setStyleSheet("background-color: none;  border: 1px solid none;")

        # self.address.setGeometry(QtCore.QRect(130, 110, 1000, 50))
        # self.address.setWordWrap(True)
        # font_address = QtGui.QFont('Arial', 20)
        # font_address.setItalic(True)
        # # self.address.setFont(font_address)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 19))

        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def video_run(self):
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.name_nv.setText(_translate("MainWindow", "Họ và Tên : "))
        self.time_log.setText(_translate("MainWindow", "Thời gian:"))
        self.temp.setText(_translate("MainWindow", "Nhiệt độ:"))
        self.position.setText(_translate("MainWindow", "Chức vụ:"))
        # # self.address.setText(_translate("MainWindow", "Địa chỉ: {}".format(address_congty)))
        self.mnv.setText(_translate("MainWindow", "Mã nhân viên:"))
        self.web.setText(_translate("MainWindow", ""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.move(0,0)
    MainWindow.show()
    sys.exit(app.exec_())

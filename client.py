from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)
        
        self.labelHostname = QLabel("Hostname :", self)
        self.labelHostname.move(0, 5)
        self.textHostname = QLineEdit(self)
        self.textHostname.move(70, 0)

        self.labelAPI_Key = QLabel("API Key :", self)
        self.labelAPI_Key.move(0, 35)
        self.textAPI_Key = QLineEdit(self)
        self.textAPI_Key.move(70, 35)

        self.labelIP_Addr = QLabel("IP Addr :", self)
        self.labelIP_Addr.move(0, 65)
        self.textIP_Addr = QLineEdit(self)
        self.textIP_Addr.move(70, 65)

        self.button = QPushButton("Send", self)
        self.button.move(85, 95)
        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.labelOrga = QLabel("Organization : ", self)
        self.labelOrga.move(0, 125)
        self.answerOrga = QLabel("", self)
        self.answerOrga.move(90, 125)

        self.labelCountry = QLabel("Country : ", self)
        self.labelCountry.move(0, 155)
        self.answerCountry = QLabel("", self)
        self.answerCountry.move(60, 155)
        self.labelLatitude = QLabel("Latitude : ", self)
        self.labelLatitude.move(0, 185)
        self.answerLatitude = QLabel("", self)
        self.answerLatitude.move(60, 185)
        self.labelLongitude = QLabel("Longitude : ", self)
        self.labelLongitude.move(0, 215)
        self.answerLongitude = QLabel("", self)
        self.answerLongitude.move(70, 215)

        self.show()
    
    def on_click(self):
        hostname = self.textHostname.text()
        apiKey = self.textAPI_Key.text()
        ipAddr = self.textIP_Addr.text()

        if ((hostname == "") or (apiKey == "") or (ipAddr == "")):
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__querry(hostname, apiKey, ipAddr)
            if res:
                self.answerOrga.setText(res["Organization"])
                self.answerOrga.adjustSize()
                self.answerCountry.setText(res["Country"])
                self.answerCountry.adjustSize()
                self.answerLatitude.setText(str(res["Latitude"]))
                self.answerLatitude.adjustSize()
                self.answerLongitude.setText(str(res["Longitude"]))
                self.answerLongitude.adjustSize()
                self.show()

                url = "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["Latitude"], res["Longitude"])
                webbrowser.open(url, new=0, autoraise=True)

    def __querry(self, hostname, apiKey, ipAddr):
        url = "http://%s/ip/%s?key=%s" % (hostname, ipAddr, apiKey)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()
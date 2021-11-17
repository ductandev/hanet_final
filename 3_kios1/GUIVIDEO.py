from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl

from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
import os
class window1(QtWidgets.QMainWindow):
    def __init__(self):
        super(window1,self).__init__()
        self.centralwid=QtWidgets.QWidget(self)
        self.vlayout=QtWidgets.QVBoxLayout()
        self.webview=QtWebEngineWidgets.QWebEngineView()
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)

        self.webview.setUrl(QUrl("http://a22049f1-0682-3c90-af23-dd497e2a063d.2splus.com"))
        self.vlayout.addWidget(self.webview)
        self.centralwid.setLayout(self.vlayout)
        self.setCentralWidget(self.centralwid)
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex=window1()
    ex.resize(1080,960)
    sys.exit(app.exec_())

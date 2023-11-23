import sys 
from  PyQt5.QtWidgets import QApplication, QWidget,QTextEdit,QLineEdit,QMainWindow,QVBoxLayout,QHBoxLayout,QComboBox,QPushButton
from PyQt5.QtSerialPort import QSerialPortInfo,QSerialPort
from PyQt5.QtCore import QIODevice

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.listSerialPorts()
    def listSerialPorts(self):
        serialPortInfo=QSerialPortInfo()
        for serialPort in serialPortInfo.availablePorts():
            self.comboSerialPortList.addItem(serialPort.portName())

    def portDataReceived(self):
        self.textEditReceiveData.append(self.serialPort.readAll().data().decode())

    def portSendData(self):
        self.serialPort.write(self.lineEditSendData.text().encode())

    def portDisconnect(self):
        if self.serialPort.isOpen():
            self.serialPort.close()
            self.pushButtonConnect.setEnabled(True)
            self.pushButtonDisconnect.setEnabled(False)
            self.pushButtonSend.setEnabled(False)

    def portConnect(self):
        self.serialPort.setPortName(self.comboSerialPortList.currentText())
        self.serialPort.setBaudRate(QSerialPort.BaudRate.Baud9600)
        self.serialPort.setDataBits(QSerialPort.DataBits.Data8)
        self.serialPort.setParity(QSerialPort.Parity.EvenParity)
        self.serialPort.setStopBits(QSerialPort.StopBits.OneStop)
        if not self.serialPort.isOpen():
            self.serialPort.open(QIODevice.ReadWrite)
            self.pushButtonConnect.setEnabled(False)
            self.pushButtonDisconnect.setEnabled(True)
            self.pushButtonSend.setEnabled(True)

    def initUI(self):
        self.serialPort=QSerialPort()
        self.setGeometry(20,50,800,600)
        self.setWindowTitle("SerialPort UI")
        vboxmain=QVBoxLayout()
        hbox1=QHBoxLayout()
        self.comboSerialPortList=QComboBox()
        hbox1.addWidget(self.comboSerialPortList)
        self.pushButtonConnect=QPushButton("Connect")
        self.pushButtonDisconnect=QPushButton("Disconnect")
        self.pushButtonDisconnect.setEnabled(False)
        hbox1.addWidget(self.pushButtonConnect)
        hbox1.addWidget(self.pushButtonDisconnect)
        hbox1.addStretch()
        vboxmain.addLayout(hbox1)
        hbox2=QHBoxLayout() 
        self.textEditReceiveData=QTextEdit()
        self.textEditReceiveData.setFixedSize(500,300)
        hbox2.addWidget(self.textEditReceiveData)
        vboxmain.addLayout(hbox2)
        hbox3=QHBoxLayout()
        self.lineEditSendData=QLineEdit()
        self.pushButtonSend=QPushButton("Send")
        self.pushButtonSend.setEnabled(False)
        hbox3.addWidget(self.lineEditSendData)
        hbox3.addWidget(self.pushButtonSend)
        vboxmain.addLayout(hbox3)
        vboxmain.addStretch()
        centralWidget=QWidget()
        centralWidget.setLayout(vboxmain)
        self.setCentralWidget(centralWidget)

        self.pushButtonConnect.clicked.connect(self.portConnect)
        self.pushButtonDisconnect.clicked.connect(self.portDisconnect)
        self.pushButtonSend.clicked.connect(self.portSendData)
        self.serialPort.readyRead.connect(self.portDataReceived)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Control_system(object):
    def setupUi(self, Control_system):

        Control_system.setObjectName("Control_system")
        Control_system.resize(1004, 722)
        Control_system.setFixedSize(1004, 722)

        Control_system.setWindowIcon(QtGui.QIcon("images/icon.png"))
        Control_system.setStyleSheet(
            "QMainWindow{border-image:url(images/background.jpg)}"
        )

        self.centralwidget = QtWidgets.QWidget(Control_system)
        self.centralwidget.setObjectName("centralwidget")

        # 表格显示
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(130, 170, 752, 245))
        self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(125)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setVisible(False)
        Control_system.setCentralWidget(self.centralwidget)
        self.tableWidget.setAutoFillBackground(True)

        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("机器编号"))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("烟雾值"))
        self.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("火焰值"))
        self.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem("温度值"))
        self.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem("电流值"))
        self.tableWidget.setItem(0, 5, QtWidgets.QTableWidgetItem("电压值"))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.tableWidget.item(0, 0).setFont(font)
        self.tableWidget.item(0, 1).setFont(font)
        self.tableWidget.item(0, 2).setFont(font)
        self.tableWidget.item(0, 3).setFont(font)
        self.tableWidget.item(0, 4).setFont(font)
        self.tableWidget.item(0, 5).setFont(font)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(360, 70, 300, 50))
        self.label.setObjectName("label")
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("border-image:url(images/title.png)")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(730, 480, 121, 41))
        self.pushButton.setObjectName("pushButton")

        Control_system.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Control_system)
        self.statusbar.setObjectName("statusbar")
        Control_system.setStatusBar(self.statusbar)

        self.retranslateUi(Control_system)
        QtCore.QMetaObject.connectSlotsByName(Control_system)

    def retranslateUi(self, Control_system):
        _translate = QtCore.QCoreApplication.translate
        Control_system.setWindowTitle(_translate("Control_system", "实时监控系统"))
        self.pushButton.setText(_translate("Control_system", "开始运行"))


class Control_system(QtWidgets.QMainWindow, Ui_Control_system):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.slotStart)
        # self.pushButton_2.clicked.connect(self.slotStop)

    @QtCore.pyqtSlot()
    def slotStart(self):
        self.pushButton.setEnabled(False)
        self.update_data_thread = UpdateData(self)
        self.update_data_thread.dataChanged.connect(self.onDataChanged)
        self.update_data_thread.start()

    @QtCore.pyqtSlot(int, int, str)
    def onDataChanged(self, row, column, text):
        it = self.tableWidget.item(row, column)
        if it is None:
            it = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(row, column, it)
        it.setText(text)

    @QtCore.pyqtSlot()
    def slotStop(self):
        self.update_data_thread.requestInterruption()
        self.update_data_thread.quit()
        self.update_data_thread.wait()
        self.pushButton.setEnabled(True)

class UpdateData(QtCore.QThread):
    dataChanged = QtCore.pyqtSignal(int, int, str)

    def run(self):
        cnt = 0
        while not self.isInterruptionRequested(): # <---
            cnt += 1
            self.dataChanged.emit(2, 2, str(cnt))
            time.sleep(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    w = Control_system()
    w.show()
    sys.exit(app.exec_())
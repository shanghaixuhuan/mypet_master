import sys
from PyQt5.QtWidgets import (QDialog,QApplication,QTableWidget,QAbstractItemView,
                             QVBoxLayout,QTableWidgetItem,QPushButton,
                             QHBoxLayout,QMessageBox,QWidget)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle


class ReleasePetHistory(QDialog):
    def __init__(self,UserId):
        super(ReleasePetHistory,self).__init__()
        self.resize(710, 500)
        self.setWindowTitle('myPet——我发布的宠物')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.UserId = UserId
        self.petCount = 0
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/myPet.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.petCount)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['备案编号', '宠物状态', '动物种类','出现地点','出现时间','收留地点'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(5).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.setColumnWidth(0,120)
        self.tableWidget.setColumnWidth(1,90)
        self.tableWidget.setColumnWidth(2,90)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,150)
        self.tableWidget.setColumnWidth(5,100)

        self.layout.addWidget(self.tableWidget)
        self.setRows()

    def getResult(self):

        sql = "select pet.PetId,PetStatus,PetType,FromLocation,FromTime,StayLocation " \
              "from pet,pet_detail " \
              "where pet.PetId = pet_detail.PetId " \
              "and pet.ReleaseUserId = '%s' " \
              "order by pet.PetId desc" %(self.UserId)

        self.query.exec_(sql)
        self.petCount = 0;
        while (self.query.next()):
            self.petCount += 1;

        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.petCount):
            if (self.query.next()):
                PetIdItem = QTableWidgetItem(self.query.value(0))
                PetStatusItem = QTableWidgetItem(self.query.value(1))
                PetTypeItem = QTableWidgetItem(self.query.value(2))
                FromLocationItem = QTableWidgetItem(self.query.value(3))
                FromTimeItem = QTableWidgetItem(self.query.value(4))
                StayLocationItem = QTableWidgetItem(self.query.value(5))

                PetIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                PetStatusItem.setFont(QFont("苏新诗柳楷繁", 12))
                PetTypeItem.setFont(QFont("苏新诗柳楷繁", 12))
                FromLocationItem.setFont(QFont("苏新诗柳楷繁", 12))
                FromTimeItem.setFont(QFont("苏新诗柳楷繁", 12))
                StayLocationItem.setFont(QFont("苏新诗柳楷繁", 12))

                PetIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                PetStatusItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                PetTypeItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                FromLocationItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                FromTimeItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StayLocationItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                self.tableWidget.setItem(i, 0, PetIdItem)
                self.tableWidget.setItem(i, 1, PetStatusItem)
                self.tableWidget.setItem(i, 2, PetTypeItem)
                self.tableWidget.setItem(i, 3, FromLocationItem)
                self.tableWidget.setItem(i, 4, FromTimeItem)
                self.tableWidget.setItem(i, 5, StayLocationItem)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    releasepethistorydialog = ReleasePetHistory('csxuhuan')
    releasepethistorydialog.show()
    sys.exit(app.exec_())

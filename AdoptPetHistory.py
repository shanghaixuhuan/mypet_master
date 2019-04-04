import sys
from PyQt5.QtWidgets import (QDialog,QApplication,QTableWidget,QAbstractItemView,
                             QVBoxLayout,QTableWidgetItem)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle


class AdoptPetHistory(QDialog):
    def __init__(self,UserId):
        super(AdoptPetHistory,self).__init__()
        self.resize(1150,600)
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
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['申请编号', '宠物编号', '申请状态','动物种类','宠物发布人','发布人邮箱','申请时间','申请理由'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(5).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(6).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(7).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.setColumnWidth(0,120)
        self.tableWidget.setColumnWidth(1,120)
        self.tableWidget.setColumnWidth(2,90)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,110)
        self.tableWidget.setColumnWidth(5,200)
        self.tableWidget.setColumnWidth(6,160)
        self.tableWidget.setColumnWidth(7,250)
        self.tableWidget.verticalHeader().setDefaultSectionSize(80)

        self.layout.addWidget(self.tableWidget)
        self.setRows()

    def getResult(self):
        sql = "select AdoptApplyId,adoptapply.AdoptPetId,AdoptStatus,PetType,UserName,UserMail,AdoptTime,AdoptText " \
              "from adoptapply,pet_detail,user " \
              "where adoptapply.AdoptFromId = user.UserId " \
              "and adoptapply.AdoptPetId = pet_detail.PetId " \
              "and adoptapply.AdoptFromId = '%s'" %(self.UserId)
        self.query.exec_(sql)
        self.petCount = 0;
        while (self.query.next()):
            self.petCount += 1;
        sql = "select AdoptApplyId,adoptapply.AdoptPetId,AdoptStatus,PetType,UserName,UserMail,AdoptTime,AdoptText " \
              "from adoptapply,pet_detail,user " \
              "where adoptapply.AdoptFromId = user.UserId " \
              "and adoptapply.AdoptPetId = pet_detail.PetId " \
              "and adoptapply.AdoptFromId = '%s'" %(self.UserId)
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.petCount):
            if (self.query.next()):
                ApplyIdItem = QTableWidgetItem(self.query.value(0))
                PetIdItem = QTableWidgetItem(self.query.value(1))
                ApplyStatusItem = QTableWidgetItem(self.query.value(2))
                PetTypeItem = QTableWidgetItem(self.query.value(3))
                ReleaseNameItem = QTableWidgetItem(self.query.value(4))
                ReleaseMailItem = QTableWidgetItem(self.query.value(5))
                ApplyTimeItem = QTableWidgetItem(self.query.value(6))
                ApplyReasonItem = QTableWidgetItem(self.query.value(7))

                ApplyIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                PetIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                ApplyStatusItem.setFont(QFont("苏新诗柳楷繁", 12))
                PetTypeItem.setFont(QFont("苏新诗柳楷繁", 12))
                ReleaseNameItem.setFont(QFont("苏新诗柳楷繁", 12))
                ReleaseMailItem.setFont(QFont("苏新诗柳楷繁", 12))
                ApplyTimeItem.setFont(QFont("苏新诗柳楷繁", 12))
                ApplyReasonItem.setFont(QFont("苏新诗柳楷繁", 12))

                ApplyIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                PetIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ApplyStatusItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                PetTypeItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ReleaseNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ReleaseMailItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ApplyTimeItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ApplyReasonItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                self.tableWidget.setItem(i, 0, ApplyIdItem)
                self.tableWidget.setItem(i, 1, PetIdItem)
                self.tableWidget.setItem(i, 2, ApplyStatusItem)
                self.tableWidget.setItem(i, 3, PetTypeItem)
                self.tableWidget.setItem(i, 4, ReleaseNameItem)
                self.tableWidget.setItem(i, 5, ReleaseMailItem)
                self.tableWidget.setItem(i, 6, ApplyTimeItem)
                self.tableWidget.setItem(i, 7, ApplyReasonItem)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    adoptpethistorydialog = AdoptPetHistory('shengzeyu')
    adoptpethistorydialog.show()
    sys.exit(app.exec_())

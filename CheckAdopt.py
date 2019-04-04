import sys
import time
from PyQt5.QtWidgets import (QDialog,QApplication,QTableWidget,QAbstractItemView,
                             QVBoxLayout,QTableWidgetItem,QPushButton,QHBoxLayout,
                             QWidget,QMessageBox)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle


class CheckAdoptDialog(QDialog):
    def __init__(self,adminid):
        super(CheckAdoptDialog,self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('myPet——审核申请')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.applyCount = 0
        self.userid = ""
        self.petid = ""
        self.adminid = adminid
        self.initUI()

    def initUI(self):

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/myPet.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()

        self.agreeid = ""
        self.disagreeid = ""
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.applyCount)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['申请编号', '用户名', '宠物编号','申请理由','申请时间'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.verticalHeader().setDefaultSectionSize(80)
        self.tableWidget.itemClicked.connect(self.getUserInfo)
        self.tableWidget.setColumnWidth(0,110)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,110)
        self.tableWidget.setColumnWidth(3,260)
        self.tableWidget.setColumnWidth(4,160)

        self.layout.addWidget(self.tableWidget)
        self.setRows()

        self.disagreeButton = QPushButton()
        self.disagreeButton.setText("驳回")
        self.disagreeButton.setFixedSize(100,40)
        self.disagreeButton.setFont(QFont("苏新诗柳楷繁", 15))
        self.disagreeButton.clicked.connect(self.disagree)

        self.agreeButton = QPushButton()
        self.agreeButton.setText("通过审核")
        self.agreeButton.setFixedSize(120,40)
        self.agreeButton.setFont(QFont("苏新诗柳楷繁", 15))
        self.agreeButton.clicked.connect(self.agree)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.disagreeButton)
        hlayout.addWidget(self.agreeButton)

        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(85)
        self.layout.addWidget(self.widget, Qt.AlignCenter)

    def getResult(self):
        sql = "select * from adoptapply where AdoptStatus = '审核中'"
        self.query.exec_(sql)
        self.applyCount = 0;
        while (self.query.next()):
            self.applyCount += 1;
        sql = "select * from adoptapply where AdoptStatus = '审核中'"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.applyCount):
            if (self.query.next()):
                AdoptApplyIdItem = QTableWidgetItem(self.query.value(0))
                AdoptUserIdItem = QTableWidgetItem(self.query.value(1))
                AdoptPetIdItem = QTableWidgetItem(self.query.value(2))
                AdoptReasonItem = QTableWidgetItem(self.query.value(4))
                AdoptTimeItem = QTableWidgetItem(self.query.value(5))
                AdoptApplyIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                AdoptUserIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                AdoptPetIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                AdoptReasonItem.setFont(QFont("苏新诗柳楷繁", 12))
                AdoptTimeItem.setFont(QFont("苏新诗柳楷繁", 12))

                AdoptApplyIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                AdoptUserIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                AdoptPetIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                AdoptReasonItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                AdoptReasonItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, AdoptApplyIdItem)
                self.tableWidget.setItem(i, 1, AdoptUserIdItem)
                self.tableWidget.setItem(i, 2, AdoptPetIdItem)
                self.tableWidget.setItem(i, 3, AdoptReasonItem)
                self.tableWidget.setItem(i, 4, AdoptTimeItem)
        return

    def getUserInfo(self):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getResult()
        i = 0
        while (self.query.next() and i != row):
            i = i + 1
        self.agreeid = self.query.value(0)
        self.userid = self.query.value(1)
        self.petid = self.query.value(2)
        self.disagreeid = self.query.value(0)

    def disagree(self):
        if(self.disagreeid == ""):
            print(QMessageBox.warning(self, "警告", "您没有选中任何申请", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "提醒", "将申请编号为%s的申请拒绝，是否继续？"
                                                % (self.disagreeid),
                                    QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.No):
            return
        sql = "update adoptapply set AdoptStatus = '被驳回' where AdoptApplyId = '%s'" %(self.disagreeid)
        self.query.exec_(sql)
        self.db.commit()
        print(QMessageBox.information(self, "提醒", "成功驳回该条申请", QMessageBox.Yes, QMessageBox.Yes))
        self.updateUI()
        return

    def agree(self):
        if (self.agreeid == ""):
            print(QMessageBox.warning(self, "警告", "您没有选中任何申请", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "提醒", "通过申请编号为%s的申请，同时自动驳回其他人对宠物的申请，是否继续？"
                                                % (self.agreeid),
                                    QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.No):
            return
        #先将通过的宠物申请的申请编号的宠物下的所有申请驳回
        sql = "update adoptapply set AdoptStatus = '被驳回' " \
              "where AdoptPetId = " \
              "(select AdoptPetId " \
              "from adoptapply " \
              "where AdoptApplyId = '%s')" %(self.agreeid)
        self.query.exec_(sql)
        self.db.commit()
        #再将通过的宠物申请状态改回通过
        sql = "update adoptapply set AdoptStatus = '已通过' " \
              "where AdoptApplyId = '%s'" %(self.agreeid)
        self.query.exec_(sql)
        self.db.commit()
        #再将通过的宠物申请的宠物状态变为已领养
        sql = "update pet set PetStatus = '已领养' " \
              "where PetId = " \
              "(select AdoptPetId " \
              "from adoptapply " \
              "where AdoptApplyId = '%s')" %(self.agreeid)
        self.query.exec_(sql)
        self.db.commit()
        #再将通过的宠物申请登记到adopt表中
        now = int(time.time())
        timeStruct = time.localtime(now)
        self.strTime = time.strftime("%Y/%m/%d %H:%M", timeStruct)
        sql = "insert into adopt values('%s','%s','%s')"%(self.petid,self.userid,self.strTime)
        self.query.exec_(sql)
        self.db.commit()
        print(QMessageBox.information(self, "提醒", "成功通过该条申请", QMessageBox.Yes, QMessageBox.Yes))
        self.updateUI()
        return

    def updateUI(self):
        self.getResult()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)
        self.agreeid = ""
        self.disagreeid = ""
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.applyCount)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['申请编号', '用户名', '宠物编号', '申请理由', '申请时间'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.verticalHeader().setDefaultSectionSize(80)
        self.tableWidget.itemClicked.connect(self.getUserInfo)
        self.tableWidget.setColumnWidth(0, 110)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 110)
        self.tableWidget.setColumnWidth(3, 260)
        self.tableWidget.setColumnWidth(4, 160)

        self.layout.addWidget(self.tableWidget)
        self.setRows()

        self.disagreeButton = QPushButton()
        self.disagreeButton.setText("驳回")
        self.disagreeButton.setFixedSize(100, 40)
        self.disagreeButton.setFont(QFont("苏新诗柳楷繁", 15))
        self.disagreeButton.clicked.connect(self.disagree)

        self.agreeButton = QPushButton()
        self.agreeButton.setText("通过审核")
        self.agreeButton.setFixedSize(120, 40)
        self.agreeButton.setFont(QFont("苏新诗柳楷繁", 15))
        self.agreeButton.clicked.connect(self.agree)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.disagreeButton)
        hlayout.addWidget(self.agreeButton)

        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(85)
        self.layout.addWidget(self.widget, Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    checkadoptDialog = CheckAdoptDialog('admin')
    checkadoptDialog.show()
    sys.exit(app.exec_())

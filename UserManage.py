import sys
import random
import time
from PyQt5.QtWidgets import (QDialog,QApplication,QTableWidget,QAbstractItemView,
                             QHeaderView,QVBoxLayout,QTableWidgetItem,QPushButton,
                             QHBoxLayout,QComboBox,QMessageBox,QWidget)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle


class UserManageDialog(QDialog):
    def __init__(self,adminid):
        super(UserManageDialog,self).__init__()
        self.resize(400, 500)
        self.setWindowTitle('myPet——用户管理')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.adminid = adminid
        self.userCount = 0
        self.alterId = ""
        self.alterName = ""
        self.alterAuthority = ""
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/myPet.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['用户名', '姓名', '用户权限'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))

        self.layout.addWidget(self.tableWidget)
        self.setRows()

        self.alterAuthorityButton = QPushButton(self)
        self.alterAuthorityButton.setText('修改权限')
        self.alterAuthorityButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.alterAuthorityButton.setFixedSize(150,50)

        self.alterAuthorityComboBox = QComboBox()
        alterAuthority = ['设为普通用户','设为灰名单','设为黑名单']
        self.alterAuthorityComboBox.setFont(QFont("苏新诗柳楷繁",12))
        self.alterAuthorityComboBox.setFixedHeight(30)
        self.alterAuthorityComboBox.addItems(alterAuthority)
        self.alterAuthorityComboBox.setFixedSize(150,50)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.alterAuthorityComboBox)
        hlayout.addStretch(1)
        hlayout.addWidget(self.alterAuthorityButton)

        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(85)
        self.layout.addWidget(self.widget, Qt.AlignCenter)

        self.tableWidget.itemClicked.connect(self.getUserInfo)
        self.alterAuthorityButton.clicked.connect(self.alterAuth)

    def getResult(self):
        sql = "select UserId,UserName,UserAuthority from user where User_isAdmin is False"
        self.query.exec_(sql)
        self.userCount = 0;
        while (self.query.next()):
            self.userCount += 1;
        sql = "select UserId,UserName,UserAuthority from user where User_isAdmin is False"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.userCount):
            if (self.query.next()):
                UserIdItem = QTableWidgetItem(self.query.value(0))
                UserNameItem = QTableWidgetItem(self.query.value(1))
                UserAuthorityItem = QTableWidgetItem(self.query.value(2))
                UserIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                UserNameItem.setFont(QFont("苏新诗柳楷繁", 12))
                UserAuthorityItem.setFont(QFont("苏新诗柳楷繁", 12))

                UserIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                UserNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                UserAuthorityItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, UserIdItem)
                self.tableWidget.setItem(i, 1, UserNameItem)
                self.tableWidget.setItem(i, 2, UserAuthorityItem)
        return

    def getUserInfo(self):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getResult()
        i = 0
        while (self.query.next() and i != row):
            i = i + 1
        self.alterId = self.query.value(0)
        self.alterName = self.query.value(1)
        self.alterAuthority = self.query.value(2)

    def alterAuth(self):
        if (self.alterId == "" and self.alterName == "" and self.alterAuthority == ""):
            print(QMessageBox.warning(self, "警告", "您没有选中任何用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        toAuthority = self.alterAuthorityComboBox.currentText()
        if(toAuthority == "设为普通用户"):
            toAuthority = "普通用户"
        elif(toAuthority == "设为灰名单"):
            toAuthority = "灰名单"
        else:
            toAuthority = "黑名单"
        if (QMessageBox.information(self, "提醒", "修改用户:%s,%s\n为 %s 权限，是否继续？"
                                                % (self.alterId, self.alterName,toAuthority),
                                    QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.No):
            return
        sql = "update user set UserAuthority = '%s' where UserId = '%s'" %(toAuthority,self.alterId)
        self.query.exec_(sql)
        self.db.commit()
        self.usermanageid = 'm' + str(time.strftime("%g%m%d")) + str(random.randint(0, 9999)).zfill(4)
        now = int(time.time())
        timeStruct = time.localtime(now)
        self.strTime = time.strftime("%Y/%m/%d %H:%M", timeStruct)
        #usermanage表插入用户管理记录
        sql = "insert into usermanage values('%s','%s','%s','%s','设为%s')" %(self.usermanageid,self.adminid,self.alterId,self.strTime,toAuthority)
        self.query.exec_(sql)
        self.db.commit()
        if(toAuthority == '灰名单' or toAuthority == '黑名单'):
            sql = "update adoptapply set AdoptStatus = '被驳回' " \
                  "where AdoptStatus = '审核中' and AdoptFromId = '%s'" %(self.alterId)
            self.query.exec_(sql)
            self.db.commit()
        print(QMessageBox.information(self, "提醒", "成功修改用户权限!", QMessageBox.Yes, QMessageBox.Yes))
        self.updateUI()
        return

    def updateUI(self):
        self.getResult()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['用户名', '姓名', '用户权限'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))

        self.layout.addWidget(self.tableWidget)
        self.setRows()

        self.alterAuthorityButton = QPushButton(self)
        self.alterAuthorityButton.setText('修改权限')
        self.alterAuthorityButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.alterAuthorityButton.setFixedSize(150, 50)

        self.alterAuthorityComboBox = QComboBox()
        alterAuthority = ['设为普通用户', '设为灰名单', '设为黑名单']
        self.alterAuthorityComboBox.setFont(QFont("苏新诗柳楷繁", 12))
        self.alterAuthorityComboBox.setFixedHeight(30)
        self.alterAuthorityComboBox.addItems(alterAuthority)
        self.alterAuthorityComboBox.setFixedSize(150, 50)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.alterAuthorityComboBox)
        hlayout.addStretch(1)
        hlayout.addWidget(self.alterAuthorityButton)

        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(85)
        self.layout.addWidget(self.widget, Qt.AlignCenter)

        self.tableWidget.itemClicked.connect(self.getUserInfo)
        self.alterAuthorityButton.clicked.connect(self.alterAuth)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    usermanageDialog = UserManageDialog('admin')
    usermanageDialog.show()
    sys.exit(app.exec_())

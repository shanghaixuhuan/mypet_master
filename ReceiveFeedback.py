import sys
from PyQt5.QtWidgets import (QDialog,QApplication,QTableWidget,QAbstractItemView,
                             QVBoxLayout,QTableWidgetItem,QPushButton,
                             QHBoxLayout,QMessageBox,QWidget)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle


class ReceiveFeedbackDialog(QDialog):
    def __init__(self):
        super(ReceiveFeedbackDialog,self).__init__()
        self.resize(700, 500)
        self.setWindowTitle('myPet——用户反馈')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.feedbackCount = 0
        self.readid = ""
        self.deleteid = ""
        self.odeleteid = ""
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/myPet.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.feedbackCount)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['反馈编号', '姓名', '反馈日期','状态','反馈信息'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setColumnWidth(0,110)
        self.tableWidget.setColumnWidth(1,60)
        self.tableWidget.setColumnWidth(2,160)
        self.tableWidget.setColumnWidth(3,60)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.verticalHeader().setDefaultSectionSize(100)
        self.tableWidget.itemClicked.connect(self.getFeedbackInfo)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.readButton = QPushButton(self)
        self.readButton.setText('标为已读')
        self.readButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.readButton.setFixedHeight(50)
        self.readButton.setFixedWidth(120)
        self.readButton.clicked.connect(self.setRead)

        self.deleteButton = QPushButton(self)
        self.deleteButton.setText('删除反馈')
        self.deleteButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.deleteButton.setFixedHeight(50)
        self.deleteButton.setFixedWidth(120)
        self.deleteButton.clicked.connect(self.deleteFeedback)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.readButton)
        hlayout.addWidget(self.deleteButton)

        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(85)
        self.layout.addWidget(self.widget, Qt.AlignCenter)

    def getResult(self):
        sql = "select FeedbackId,UserName,FeedbackTime,FeedBackStatus,FeedbackText " \
              "from feedback,user where feedback.FeedbackUserId = user.UserId " \
              "order by FeedbackTime desc"
        self.query.exec_(sql)
        self.feedbackCount = 0;
        while (self.query.next()):
            self.feedbackCount += 1;
        sql = "select FeedbackId,UserName,FeedbackTime,FeedBackStatus,FeedbackText " \
              "from feedback,user where feedback.FeedbackUserId = user.UserId " \
              "order by FeedbackTime desc"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.feedbackCount):
            if (self.query.next()):
                FeedbackIdItem = QTableWidgetItem(self.query.value(0))
                UserNameItem = QTableWidgetItem(self.query.value(1))
                FeedbackTimeItem = QTableWidgetItem(self.query.value(2))
                FeedbackStatusItem = QTableWidgetItem(self.query.value(3))
                FeedbackTextItem = QTableWidgetItem(self.query.value(4))

                FeedbackIdItem.setFont(QFont("苏新诗柳楷繁", 12))
                UserNameItem.setFont(QFont("苏新诗柳楷繁", 12))
                FeedbackTimeItem.setFont(QFont("苏新诗柳楷繁", 12))
                FeedbackStatusItem.setFont(QFont("苏新诗柳楷繁", 12))
                FeedbackTextItem.setFont(QFont("苏新诗柳楷繁", 12))

                FeedbackIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                UserNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                FeedbackTimeItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                FeedbackStatusItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                self.tableWidget.setItem(i, 0, FeedbackIdItem)
                self.tableWidget.setItem(i, 1, UserNameItem)
                self.tableWidget.setItem(i, 2, FeedbackTimeItem)
                self.tableWidget.setItem(i, 3, FeedbackStatusItem)
                self.tableWidget.setItem(i, 4, FeedbackTextItem)
        return

    def setRead(self):
        if(self.readid == ""):
            print(QMessageBox.warning(self, "警告", "您没有选中任何反馈信息", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "提醒", "将反馈设为已读，是否继续？",
                                    QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.No):
            return
        sql = "update feedback set FeedBackStatus = '已读' where FeedbackId = '%s'" %(self.readid)
        self.query.exec_(sql)
        self.db.commit()
        print(QMessageBox.information(self, "提醒", "已将消息设为已读！", QMessageBox.Yes, QMessageBox.Yes))
        self.updateUI()
        return

    def deleteFeedback(self):
        if (self.deleteid == ""):
            print(QMessageBox.warning(self, "警告", "您没有选中任何反馈信息", QMessageBox.Yes, QMessageBox.Yes))
            return
        if(self.deleteid == self.odeleteid):
            print(QMessageBox.warning(self, "警告", "您没有选中任何反馈信息", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "提醒", "删除消息:%s\n一经删除将无法恢复，是否继续?"
                                                % (self.deleteid),
                                    QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.No):
            return
        sql = "delete from feedback where FeedbackId = '%s'" %(self.deleteid)
        self.query.exec_(sql)
        self.db.commit()
        print(QMessageBox.information(self, "提醒", "删除反馈信息成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.updateUI()
        return

    def getFeedbackInfo(self):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getResult()
        i = 0
        while (self.query.next() and i != row):
            i = i + 1
        self.odeleteid = self.deleteid
        self.deleteid = self.query.value(0)
        self.readid = self.query.value(0)

    def updateUI(self):
        self.getResult()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.feedbackCount)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['反馈编号', '姓名', '反馈日期', '状态', '反馈信息'])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeaderItem(0).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(1).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(2).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(3).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.horizontalHeaderItem(4).setFont(QFont("苏新诗柳楷繁", 12))
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setColumnWidth(0, 110)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 160)
        self.tableWidget.setColumnWidth(3, 60)
        self.tableWidget.setColumnWidth(4, 250)
        self.tableWidget.verticalHeader().setDefaultSectionSize(100)
        self.tableWidget.itemClicked.connect(self.getFeedbackInfo)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.readButton = QPushButton(self)
        self.readButton.setText('标为已读')
        self.readButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.readButton.setFixedHeight(50)
        self.readButton.setFixedWidth(120)
        self.readButton.clicked.connect(self.setRead)

        self.deleteButton = QPushButton(self)
        self.deleteButton.setText('删除反馈')
        self.deleteButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.deleteButton.setFixedHeight(50)
        self.deleteButton.setFixedWidth(120)
        self.deleteButton.clicked.connect(self.deleteFeedback)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.readButton)
        hlayout.addWidget(self.deleteButton)

        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(85)
        self.layout.addWidget(self.widget, Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    receivefeedbackDialog = ReceiveFeedbackDialog()
    receivefeedbackDialog.show()
    sys.exit(app.exec_())

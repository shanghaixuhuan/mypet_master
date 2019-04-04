import sys
import time
import random
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QTextEdit,QPushButton,QMessageBox)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtSql import QSqlDatabase,QSqlQuery


class FeedBackDialog(QDialog):
    def __init__(self,UserId):
        super(FeedBackDialog,self).__init__()
        self.UserId = UserId
        self.initUI()

    def initUI(self):
        self.resize(500,550)
        self.setWindowTitle("myPet——反馈信息")
        self.setWindowIcon(QIcon("./images/icon.png"))

        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('./images/title.png')
        self.titlelabel.setPixmap(self.titleimage)
        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.textedit = QTextEdit()
        self.textedit.setFixedSize(400,250)
        self.textedit.setFont(QFont("苏新诗柳楷繁", 13))
        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.textedit)
        self.h2box.addStretch(1)

        self.clearbutton = QPushButton()
        self.clearbutton.setFixedSize(100,40)
        self.clearbutton.setText("清空")
        self.clearbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.clearbutton.clicked.connect(self.clear)
        self.submitbutton = QPushButton()
        self.submitbutton.setFixedSize(100, 40)
        self.submitbutton.setText("提交")
        self.submitbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.submitbutton.clicked.connect(self.submit)
        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.clearbutton)
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.submitbutton)
        self.h3box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

    def submit(self):
        self.text = self.textedit.toPlainText()
        self.feedbackid = 'f' + str(time.strftime("%g%m%d")) + str(random.randint(0, 9999)).zfill(4)
        now = int(time.time())
        timeStruct = time.localtime(now)
        self.strTime = time.strftime("%Y/%m/%d %H:%M", timeStruct)
        if(len(self.text) < 15):
            print(QMessageBox.warning(self, "警告", "无法提交少于15字的反馈。", QMessageBox.Yes, QMessageBox.Yes))
            return
        if(len(self.text) > 200):
            print(QMessageBox.warning(self, "警告", "无法提交大于200字的反馈", QMessageBox.Yes, QMessageBox.Yes))
            return
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/myPet.db')
        db.open()
        query = QSqlQuery()
        sql = "select * from feedback where FeedbackId = '%s'" %(self.feedbackid)
        query.exec_(sql)
        if (query.next()):  # 反馈编号已存在
            print(QMessageBox.warning(self, "警告", "系统错误，请重新提交", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            sql = "insert into feedback values('%s','%s','%s','未读','%s')" % (self.feedbackid,self.UserId,self.strTime,self.text)
            query.exec_(sql)
            db.commit()
            db.close()
            print(QMessageBox.information(self, "提醒", "您已成功提交反馈信息!", QMessageBox.Yes, QMessageBox.Yes))
            self.textedit.setText("")

    def clear(self):
        self.textedit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    aboutWindow = FeedBackDialog('csxuhuan')
    aboutWindow.show()
    sys.exit(app.exec_())
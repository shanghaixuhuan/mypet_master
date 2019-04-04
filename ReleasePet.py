import sys
import qdarkstyle
import time
import random
from PyQt5.QtWidgets import (QDialog,QApplication,QLabel,QPushButton,
                             QFileDialog,QHBoxLayout,QVBoxLayout,QLineEdit,
                             QDateTimeEdit,QMessageBox)
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtSql import QSqlDatabase,QSqlQuery


class ReleasePetDialog(QDialog):
    def __init__(self,UserId):
        super(ReleasePetDialog,self).__init__()
        self.UserId = UserId
        self.filePath = ""
        self.type = ""
        self.froml = ""
        self.fromt = ""
        self.stayl = ""
        self.resize(800,500)
        self.setWindowTitle('myPet——发布招领')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.initUI()

    def initUI(self):
        self.plabel = QLabel(self)
        self.plabel.setFixedSize(370,370)
        self.plabel.move(20,20)
        self.hbox11 = QHBoxLayout()
        self.hbox11.addStretch(1)
        self.hbox11.addWidget(self.plabel)
        self.hbox11.addStretch(1)

        self.obtn = QPushButton(self)
        self.obtn.setText("打开本地图片")
        self.obtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.obtn.resize(200, 50)
        self.obtn.move(560, 30)
        self.obtn.clicked.connect(self.openimage)
        self.obtn.setFixedSize(180,50)
        self.hbox12 = QHBoxLayout()
        self.hbox12.addStretch(1)
        self.hbox12.addWidget(self.obtn)
        self.hbox12.addStretch(1)

        self.vbox1 = QVBoxLayout()
        self.vbox1.addLayout(self.hbox11)
        self.vbox1.addLayout(self.hbox12)

        self.typelabel = QLabel()
        self.typelabel.setText("动物种类")
        self.typelabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.typeedit = QLineEdit()
        self.typeedit.setFixedSize(180,30)
        self.typeedit.setFont(QFont("苏新诗柳楷繁", 13))
        self.hbox21 = QHBoxLayout()
        self.hbox21.addStretch(1)
        self.hbox21.addWidget(self.typelabel)
        self.hbox21.addStretch(1)
        self.hbox21.addWidget(self.typeedit)
        self.hbox21.addStretch(1)

        self.fromllabel = QLabel()
        self.fromllabel.setText("出现地点")
        self.fromllabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.fromledit = QLineEdit()
        self.fromledit.setFixedSize(180, 30)
        self.fromledit.setFont(QFont("苏新诗柳楷繁", 13))
        self.hbox22 = QHBoxLayout()
        self.hbox22.addStretch(1)
        self.hbox22.addWidget(self.fromllabel)
        self.hbox22.addStretch(1)
        self.hbox22.addWidget(self.fromledit)
        self.hbox22.addStretch(1)

        self.fromtlabel = QLabel()
        self.fromtlabel.setText("出现时间")
        self.fromtlabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.fromtedit = QDateTimeEdit()
        self.fromtedit.setFixedSize(180, 30)
        self.fromtedit.setFont(QFont("苏新诗柳楷繁", 13))
        self.hbox23 = QHBoxLayout()
        self.hbox23.addStretch(1)
        self.hbox23.addWidget(self.fromtlabel)
        self.hbox23.addStretch(1)
        self.hbox23.addWidget(self.fromtedit)
        self.hbox23.addStretch(1)

        self.stayllabel = QLabel()
        self.stayllabel.setText("收留地点")
        self.stayllabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.stayledit = QLineEdit()
        self.stayledit.setFixedSize(180, 30)
        self.stayledit.setFont(QFont("苏新诗柳楷繁", 13))
        self.hbox24 = QHBoxLayout()
        self.hbox24.addStretch(1)
        self.hbox24.addWidget(self.stayllabel)
        self.hbox24.addStretch(1)
        self.hbox24.addWidget(self.stayledit)
        self.hbox24.addStretch(1)

        self.rbtn = QPushButton(self)
        self.rbtn.setText("发布招领")
        self.rbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.rbtn.resize(200, 50)
        self.rbtn.move(560, 30)
        self.rbtn.setFixedSize(180, 50)
        self.hbox25 = QHBoxLayout()
        self.hbox25.addStretch(1)
        self.hbox25.addWidget(self.rbtn)
        self.hbox25.addStretch(1)

        self.vbox2 = QVBoxLayout()
        self.vbox2.addLayout(self.hbox21)
        self.vbox2.addLayout(self.hbox22)
        self.vbox2.addLayout(self.hbox23)
        self.vbox2.addLayout(self.hbox24)
        self.vbox2.addLayout(self.hbox25)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.setLayout(self.hbox)

        self.type = self.typeedit.text()

        self.rbtn.clicked.connect(self.rbtnClicked)

    def openimage(self):
        self.filePath, imgType = QFileDialog.getOpenFileName(self, "打开本地图片", "", "*.jpg;;*.png;;All Files(*)")
        self.jpg = QPixmap(self.filePath).scaled(self.plabel.width(), self.plabel.height())
        self.plabel.setPixmap(self.jpg)

    def rbtnClicked(self):
        self.type = self.typeedit.text()
        self.froml = self.fromledit.text()
        self.fromt = self.fromtedit.text()
        self.stayl = self.stayledit.text()
        self.petid = 'p' + str(time.strftime("%g%m%d")) + str(random.randint(0,9999)).zfill(4)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/myPet.db')
        db.open()
        query = QSqlQuery()
        sql = "select * from user where UserId = '%s' and UserAuthority = '黑名单'" %(self.UserId)
        query.exec_(sql)
        if(query.next()):
            print(QMessageBox.warning(self, "警告", "你是黑名单用户，无法发布宠物！", QMessageBox.Yes, QMessageBox.Yes))
            return
        if(self.type == "" or self.filePath == "" or self.froml == "" or self.froml == "" or self.fromt == ""):
            print(QMessageBox.warning(self, "警告", "图片未插入或信息不完整！", QMessageBox.Yes, QMessageBox.Yes))
            return
        sql = "select * from pet where PetId = '%s'"%(self.petid)
        query.exec_(sql)
        if (query.next()):  # 宠物编号已存在
            print(QMessageBox.warning(self, "警告", "系统错误，请重新提交", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            sql = "insert into pet values ('%s','待领养','%s','%s')" % (self.petid, self.UserId, self.filePath)
            query.exec_(sql)
            db.commit()
            sql = "insert into pet_detail values ('%s','%s','%s','%s','%s')" % (self.petid,self.type,self.froml,self.fromt,self.stayl)
            query.exec_(sql)
            db.commit()
            db.close()
            print(QMessageBox.information(self, "提醒", "您已成功发布领养信息!", QMessageBox.Yes, QMessageBox.Yes))
            self.stayledit.setText("")
            self.typeedit.setText("")
            self.fromledit.setText("")
            self.filePath = ""
            self.jpg = QPixmap(self.filePath).scaled(self.plabel.width(), self.plabel.height())
            self.plabel.setPixmap(self.jpg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    releasepetDialog = ReleasePetDialog('csxuhuan')
    releasepetDialog.show()
    sys.exit(app.exec_())
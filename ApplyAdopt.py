import sys
import time
import random
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QLineEdit,QPushButton,QMessageBox,
                             QPlainTextEdit)
import qdarkstyle
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtSql import QSqlDatabase,QSqlQuery


class ApplyAdoptDialog(QDialog):
    def __init__(self,UserId):
        super(ApplyAdoptDialog,self).__init__()
        self.userid = UserId
        self.initUI()

    def initUI(self):
        self.resize(400,350)
        self.setWindowTitle("myPet——宠物领养")
        self.setWindowIcon(QIcon("./images/icon.png"))

        self.idlabel = QLabel(self)
        self.idlabel.setText("备案编号：")
        self.idlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.idedit = QLineEdit()
        self.idedit.setFixedSize(300,35)
        self.idedit.setFont(QFont("苏新诗柳楷繁", 13))
        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.idlabel)
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.idedit)
        self.h1box.addStretch(1)

        self.textlabel = QLabel(self)
        self.textlabel.setText("申请理由：")
        self.textlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.textedit = QPlainTextEdit()
        self.textedit.setFixedSize(300,150)
        self.textedit.setFont(QFont("苏新诗柳楷繁", 13))
        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.textlabel)
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.textedit)
        self.h2box.addStretch(1)

        self.submitbutton = QPushButton()
        self.submitbutton.setText("申请领养")
        self.submitbutton.setFixedSize(150,35)
        self.submitbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.submitbutton.clicked.connect(self.submit)
        self.h3box = QHBoxLayout()
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
        self.adoptid = 'a' + str(time.strftime("%g%m%d")) + str(random.randint(0, 9999)).zfill(4)
        self.petid = self.idedit.text()
        self.adopttext = self.textedit.toPlainText()
        now = int(time.time())
        timeStruct = time.localtime(now)
        self.strTime = time.strftime("%Y/%m/%d %H:%M", timeStruct)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("./db/myPet.db")
        db.open()
        query = QSqlQuery()
        sql = "select * from user where UserId = '%s' and UserAuthority = '黑名单'" % (self.userid)
        query.exec_(sql)
        if (query.next()):
            print(QMessageBox.warning(self, "警告", "你是黑名单用户，无法申请宠物领养！", QMessageBox.Yes, QMessageBox.Yes))
            return
        sql = "select * from user where UserId = '%s' and UserAuthority = '灰名单'" % (self.userid)
        query.exec_(sql)
        if (query.next()):
            print(QMessageBox.warning(self, "警告", "你是灰名单用户，无法申请宠物领养！", QMessageBox.Yes, QMessageBox.Yes))
            return
        if(self.petid == ""):
            print(QMessageBox.warning(self, "警告", "请输入备案编号！", QMessageBox.Yes, QMessageBox.Yes))
            return
        #先查看拟定领养宠物是否存在
        sql = "select * from pet where PetId = '%s'" %(self.petid)
        query.exec_(sql)
        if(query.next()):
            #查看是否为自己领养自己的宠物
            sql = "select * from pet where PetId = '%s' and ReleaseUserId = '%s'" %(self.petid,self.userid)
            query.exec_(sql)
            if (query.next()):
                print(QMessageBox.warning(self, "警告", "请勿申请领养自己发布的宠物", QMessageBox.Yes, QMessageBox.Yes))
                return
            #查看宠物是否是已领养状态
            sql = "select * from pet where PetId = '%s' and PetStatus = '已领养'" %(self.petid)
            query.exec_(sql)
            if(query.next()):
                print(QMessageBox.warning(self, "警告", "宠物已被领养，无法提交申请！", QMessageBox.Yes, QMessageBox.Yes))
                return
            #查看领养编号是否重复
            sql = "select * from adoptapply where AdoptApplyId = '%s'" %(self.adoptid)
            query.exec_(sql)
            if(query.next()):
                print(QMessageBox.warning(self, "警告", "系统出错，请稍后尝试", QMessageBox.Yes, QMessageBox.Yes))
                return
            #查看是否已存在申请用户和申请宠物相同 且申请状态为“审核中”的
            sql = "select * from adoptapply where AdoptFromId = '%s' " \
                  "and AdoptPetId = '%s' and AdoptStatus = '审核中'" %(self.userid,self.petid)
            query.exec_(sql)
            if(query.next()):
                print(QMessageBox.warning(self, "警告", "您对该宠物有申请正在审核中，请勿重复提交", QMessageBox.Yes, QMessageBox.Yes))
                return
            sql = "insert into adoptapply values('%s','%s','%s','审核中','%s','%s')" %(self.adoptid,self.userid,self.petid,self.adopttext,self.strTime)
            query.exec_(sql)
            db.commit()
            db.close()
            print(QMessageBox.information(self, "提醒", "你已成功提交宠物领养申请", QMessageBox.Yes, QMessageBox.Yes))
            self.idedit.setText("")
            self.textedit.clear()
        else:
            print(QMessageBox.warning(self, "警告", "您输入的宠物备案编号并不存在，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    applyadoptdialog = ApplyAdoptDialog('csxuhuan')
    applyadoptdialog.show()
    sys.exit(app.exec_())
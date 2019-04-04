import sys
import hashlib
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QHBoxLayout,
                             QVBoxLayout,QLineEdit,QPushButton,QMessageBox)
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtSql import QSqlQuery,QSqlDatabase
from PyQt5.QtCore import pyqtSignal
import qdarkstyle


class SignInWidget(QWidget):
    is_admin_signal = pyqtSignal(str)
    is_user_signal = pyqtSignal(str)

    def __init__(self):
        super(SignInWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800,600)
        self.setWindowTitle('myPet——欢迎使用宠物招领系统')
        self.setWindowIcon(QIcon('./images/icon.png'))

        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('./images/title.png')
        self.titlelabel.setPixmap(self.titleimage)
        self.titlelabel.move(200,30)

        self.idlabel = QLabel(self)
        self.idlabel.setText('用户名')
        self.idlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.idlabel.setFixedHeight(50)
        self.idedit = QLineEdit(self)
        self.idedit.setFixedWidth(200)
        self.idedit.setFixedHeight(30)
        self.idedit.setFont(QFont("苏新诗柳楷繁", 12))
        self.h1box = QHBoxLayout()
        self.h1box.addWidget(self.idlabel)
        self.h1box.addWidget(self.idedit)

        self.pswlabel = QLabel(self)
        self.pswlabel.setText('密码')
        self.pswlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.pswlabel.setFixedHeight(50)
        self.pswedit = QLineEdit(self)
        self.pswedit.setFixedWidth(200)
        self.pswedit.setFixedHeight(30)
        self.pswedit.setFont(QFont("苏新诗柳楷繁", 10))
        self.pswedit.setEchoMode(QLineEdit.Password)
        self.h2box = QHBoxLayout()
        self.h2box.addWidget(self.pswlabel)
        self.h2box.addWidget(self.pswedit)

        self.signinbutton = QPushButton(self)
        self.signinbutton.setFixedHeight(50)
        self.signinbutton.setFixedWidth(150)
        self.signinbutton.setText('登  录')
        self.signinbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.signinbutton)
        self.h3box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.titlelabel)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

        self.signinbutton.clicked.connect(self.signInCheck)
        self.idedit.returnPressed.connect(self.signInCheck)
        self.pswedit.returnPressed.connect(self.signInCheck)

    def signInCheck(self):
        id = self.idedit.text()
        psw = self.pswedit.text()
        if(id == "" or psw == ""):
            print(QMessageBox.warning(self, "警告", "账户名或密码为空！", QMessageBox.Yes, QMessageBox.Yes))
            return
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/myPet.db')
        db.open()
        query = QSqlQuery()
        sql = "select user.UserId,UserPsw,User_isAdmin " \
              "from user,user_code " \
              "where user.UserId = user_code.UserId and user.UserId = '%s'" %(id)
        query.exec_(sql)
        db.close()

        hl = hashlib.md5()
        hl.update(psw.encode(encoding = 'utf-8'))
        if(not query.next()):
            print(QMessageBox.information(self, "提示", "用户名并不存在！", QMessageBox.Yes, QMessageBox.Yes))
        else:
            if(id == query.value(0) and hl.hexdigest() == query.value(1)):
                print(QMessageBox.warning(self, "提示", "老师你对这个系统满意吗", QMessageBox.Yes, QMessageBox.Yes))
                if(query.value(2) == True):
                    self.is_admin_signal.emit(id)
                else:
                    self.is_user_signal.emit(id)
            else:
                print(QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    signinWindow = SignInWidget()
    signinWindow.show()
    sys.exit(app.exec_())

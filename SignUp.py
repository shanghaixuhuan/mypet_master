import sys
import re
import hashlib
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QHBoxLayout,
                             QVBoxLayout,QLineEdit,QPushButton,QMessageBox)
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle


class SignUpWidget(QWidget):
    def __init__(self):
        super(SignUpWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800,600)
        self.setWindowTitle('myPet——欢迎使用宠物招领系统')
        self.setWindowIcon(QIcon('./images/icon.png'))

        #标题标签组件
        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('./images/title.png')
        self.titlelabel.setPixmap(self.titleimage)
        self.titlelabel.move(200,30)

        #用户名标签组件、用户名输入框组件
        self.idlabel = QLabel(self)
        self.idlabel.setText('请输入用户名')
        self.idlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.idlabel.setFixedHeight(50)
        self.idedit = QLineEdit(self)
        self.idedit.setFixedWidth(200)
        self.idedit.setFixedHeight(30)
        self.idedit.setFont(QFont("苏新诗柳楷繁", 12))
        self.h1box = QHBoxLayout()
        self.h1box.addWidget(self.idlabel)
        self.h1box.addWidget(self.idedit)

        #密码标签组件、密码输入框组件
        self.pswlabel = QLabel(self)
        self.pswlabel.setText('请输入密码')
        self.pswlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.pswlabel.setFixedHeight(50)
        self.pswedit = QLineEdit(self)
        self.pswedit.setFixedWidth(200)
        self.pswedit.setFixedHeight(30)
        self.pswedit.setEchoMode(QLineEdit.Password)
        self.h2box = QHBoxLayout()
        self.h2box.addWidget(self.pswlabel)
        self.h2box.addWidget(self.pswedit)

        #重复输入密码标签组件、重复输入密码输入框标签
        self.againpswlabel = QLabel(self)
        self.againpswlabel.setText('请重复输入密码')
        self.againpswlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.againpswlabel.setFixedHeight(50)
        self.againpswedit = QLineEdit(self)
        self.againpswedit.setFixedWidth(200)
        self.againpswedit.setFixedHeight(30)
        self.againpswedit.setEchoMode(QLineEdit.Password)
        self.h3box = QHBoxLayout()
        self.h3box.addWidget(self.againpswlabel)
        self.h3box.addWidget(self.againpswedit)

        #姓名标签组件、姓名输入框标签
        self.namelabel = QLabel(self)
        self.namelabel.setText('请输入真实姓名')
        self.namelabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.namelabel.setFixedHeight(50)
        self.nameedit = QLineEdit(self)
        self.nameedit.setFixedWidth(200)
        self.nameedit.setFixedHeight(30)
        self.nameedit.setFont(QFont("苏新诗柳楷繁", 12))
        self.h4box = QHBoxLayout()
        self.h4box.addWidget(self.namelabel)
        self.h4box.addWidget(self.nameedit)

        #邮箱标签组件、邮箱输入框组件
        self.maillabel = QLabel(self)
        self.maillabel.setText('请输入邮箱')
        self.maillabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.maillabel.setFixedHeight(50)
        self.mailedit = QLineEdit(self)
        self.mailedit.setFixedWidth(200)
        self.mailedit.setFixedHeight(30)
        self.mailedit.setFont(QFont("苏新诗柳楷繁", 12))
        self.h5box = QHBoxLayout()
        self.h5box.addWidget(self.maillabel)
        self.h5box.addWidget(self.mailedit)

        #注册按钮组件
        self.signupbutton = QPushButton(self)
        self.signupbutton.setFixedHeight(50)
        self.signupbutton.setFixedWidth(150)
        self.signupbutton.setText('注  册')
        self.signupbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.h6box = QHBoxLayout()
        self.h6box.addStretch(1)
        self.h6box.addWidget(self.signupbutton)
        self.h6box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.titlelabel)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addLayout(self.h2box)
        self.vbox.addLayout(self.h3box)
        self.vbox.addLayout(self.h4box)
        self.vbox.addLayout(self.h5box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h6box)
        self.vbox.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

        self.signupbutton.clicked.connect(self.SignUp)
        self.idedit.returnPressed.connect(self.SignUp)
        self.pswedit.returnPressed.connect(self.SignUp)
        self.againpswedit.returnPressed.connect(self.SignUp)
        self.nameedit.returnPressed.connect(self.SignUp)
        self.mailedit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        id = self.idedit.text()
        psw = self.pswedit.text()
        againpsw = self.againpswedit.text()
        name = self.nameedit.text()
        mail = self.mailedit.text()
        if(id == '' or psw == '' or againpsw == '' or name == '' or mail == ''):#验证表单是否为空
            print(QMessageBox.warning(self, "警告", "请将所有信息填全！", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif(psw != againpsw):#验证两次输入密码是否相同
            print(QMessageBox.warning(self, "警告", "两次输入的密码不一致！", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif (psw.isalnum() == False or len(psw) < 5 or len(psw) > 20):#验证密码格式正确性
            print(QMessageBox.warning(self, "警告", "密码由长度为5-20位大小写英文字符和数字组成。", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif(id.isalnum() == False or len(id) < 5 or len(id) > 20 or id[0].isalpha() == False):#验证用户名格式正确性
            print(QMessageBox.warning(self, "警告", "用户名由长度为5-20位大小写英文字符和数字组成，且第一位必须是英文字符", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif(len(name) < 2 or len(name) >4):#验证姓名正确性
            print(QMessageBox.warning(self, "警告", "姓名由2-4位中文汉字组成", QMessageBox.Yes,QMessageBox.Yes))
            return
        else:
            for ch in name:
                if u'\u4e00' > ch or ch > u'\u9fff':
                    print(QMessageBox.warning(self, "警告", "姓名由2-4位中文汉字组成", QMessageBox.Yes, QMessageBox.Yes))
                    return
            if(re.match(r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$', mail)):#检验邮箱格式正确性
                #先打开user_code表验证是否用户名已注册
                db = QSqlDatabase.addDatabase("QSQLITE")
                db.setDatabaseName('./db/myPet.db')
                db.open()
                query = QSqlQuery()
                sql = "select * from user_code where UserId = '%s'" % (id)
                query.exec_(sql)
                if (query.next()):#用户名已被注册
                    print(QMessageBox.warning(self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:#用户名未被注册的情况下打开user表和user_code表插入新用户信息
                    hl = hashlib.md5()
                    hl.update(psw.encode(encoding='utf-8'))
                    md5psw = hl.hexdigest()
                    sql = "insert into user_code values ('%s','%s')" % (id,md5psw)
                    db.exec_(sql)
                    db.commit()
                    sql = "insert into user values('%s','%s','%s',False,'普通用户')" % (id,name,mail)
                    db.exec_(sql)
                    db.commit()
                    db.close()
                    print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                    self.idedit.setText("")
                    self.pswedit.setText("")
                    self.againpswedit.setText("")
                    self.nameedit.setText("")
                    self.mailedit.setText("")
            else:#邮箱格式错误
                print(QMessageBox.warning(self, "警告", "邮箱地址并不合法", QMessageBox.Yes, QMessageBox.Yes))
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    signupWindow = SignUpWidget()
    signupWindow.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QApplication,QDialog,QLabel,QHBoxLayout,
                             QVBoxLayout,QLineEdit,QPushButton,QMessageBox)
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle
import hashlib


class ChangePswDialog(QDialog):
    def __init__(self):
        super(ChangePswDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(700,500)
        self.setWindowTitle('myPet——欢迎使用宠物招领系统')
        self.setWindowIcon(QIcon('./images/icon.png'))

        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('./images/title.png')
        self.titlelabel.setPixmap(self.titleimage)
        self.titlelabel.move(200,30)

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

        self.pswlabel = QLabel(self)
        self.pswlabel.setText('请输入原密码')
        self.pswlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.pswlabel.setFixedHeight(50)
        self.pswedit = QLineEdit(self)
        self.pswedit.setFixedWidth(200)
        self.pswedit.setFixedHeight(30)
        self.pswedit.setEchoMode(QLineEdit.Password)
        self.h2box = QHBoxLayout()
        self.h2box.addWidget(self.pswlabel)
        self.h2box.addWidget(self.pswedit)

        self.newpswlabel = QLabel(self)
        self.newpswlabel.setText('请输入新密码')
        self.newpswlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.newpswlabel.setFixedHeight(50)
        self.newpswedit = QLineEdit(self)
        self.newpswedit.setFixedWidth(200)
        self.newpswedit.setFixedHeight(30)
        self.newpswedit.setEchoMode(QLineEdit.Password)
        self.h3box = QHBoxLayout()
        self.h3box.addWidget(self.newpswlabel)
        self.h3box.addWidget(self.newpswedit)

        self.againpswlabel = QLabel(self)
        self.againpswlabel.setText('请重复新密码')
        self.againpswlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.againpswlabel.setFixedHeight(50)
        self.againpswedit = QLineEdit(self)
        self.againpswedit.setFixedWidth(200)
        self.againpswedit.setFixedHeight(30)
        self.againpswedit.setEchoMode(QLineEdit.Password)
        self.h4box = QHBoxLayout()
        self.h4box.addWidget(self.againpswlabel)
        self.h4box.addWidget(self.againpswedit)

        self.changepswbutton = QPushButton(self)
        self.changepswbutton.setFixedHeight(50)
        self.changepswbutton.setFixedWidth(150)
        self.changepswbutton.setText('修改密码')
        self.changepswbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.changepswbutton.clicked.connect(self.changePsw)
        self.h5box = QHBoxLayout()
        self.h5box.addStretch(1)
        self.h5box.addWidget(self.changepswbutton)
        self.h5box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.titlelabel)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addLayout(self.h2box)
        self.vbox.addLayout(self.h3box)
        self.vbox.addLayout(self.h4box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h5box)
        self.vbox.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

        self.idedit.returnPressed.connect(self.changePsw)
        self.pswedit.returnPressed.connect(self.changePsw)
        self.newpswedit.returnPressed.connect(self.changePsw)
        self.againpswedit.returnPressed.connect(self.changePsw)

    def changePsw(self):
        id = self.idedit.text()
        psw = self.pswedit.text()
        againpsw = self.againpswedit.text()
        newpsw = self.newpswedit.text()
        if(id == '' or psw == '' or againpsw == '' or newpsw == ''):
            print(QMessageBox.warning(self, "警告", "请将所有信息填全！", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif(newpsw != againpsw):
            print(QMessageBox.warning(self, "警告", "两次输入的密码不一致！", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            hl = hashlib.md5()
            hl.update(psw.encode(encoding='utf-8'))
            md5psw = hl.hexdigest()
            hl_ = hashlib.md5()
            hl_.update(newpsw.encode(encoding='utf-8'))
            md5newpsw = hl_.hexdigest()
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/myPet.db')
            db.open()
            query = QSqlQuery()
            sql = "select * from user_code where UserId = '%s' and UserPsw = '%s'" % (id,md5psw)
            query.exec_(sql)
            if(query.next()):
                if(newpsw.isalnum() == False or len(newpsw) < 5 or len(newpsw) > 20):  # 验证密码格式正确性
                    print(QMessageBox.warning(self, "警告", "密码由长度为5-20位大小写英文字符和数字组成。", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:
                    sql = "update user_code set UserPsw = '%s' where UserId = '%s'" % (md5newpsw,id)
                    db.exec_(sql)
                    db.commit()
                    db.close()
                    print(QMessageBox.information(self, "提醒", "修改密码成功！", QMessageBox.Yes, QMessageBox.Yes))
                    self.idedit.setText("")
                    self.pswedit.setText("")
                    self.againpswedit.setText("")
                    self.newpswedit.setText("")
                    return
            else:
                print(QMessageBox.warning(self, "警告", "用户不存在或密码错误", QMessageBox.Yes, QMessageBox.Yes))
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    changepswDialog = ChangePswDialog()
    changepswDialog.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QWidget,QApplication,QHBoxLayout,QVBoxLayout,
                             QPushButton,QLabel)
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import qdarkstyle
from PetViewer import PetViewer
from ReleasePet import ReleasePetDialog
from FeedBack import FeedBackDialog
from ApplyAdopt import ApplyAdoptDialog
from ReleasePetHistory import ReleasePetHistory
from AdoptPetHistory import AdoptPetHistory


class UserHome(QWidget):
    def __init__(self,UserId):
        super(UserHome,self).__init__()
        self.UserId = UserId
        self.resize(800,600)
        self.setWindowTitle('myPet——用户界面')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./db/myPet.db')
        self.db.open()
        self.query = QSqlQuery()
        sql = "select * from user where UserId = '%s'" %(self.UserId)
        self.query.exec_(sql)
        self.query.next()
        name = self.query.value(1)
        authority = self.query.value(4)

        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('./images/title.png')
        self.titlelabel.setPixmap(self.titleimage)
        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.whelcomelabel = QLabel()
        self.whelcomelabel.setText("    欢迎 " + name + " 登录\n你的用户权限是：" + authority)
        self.whelcomelabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.whelcomelabel)
        self.h2box.addStretch(1)

        self.checkallpetbutton = QPushButton()
        self.checkallpetbutton.setFixedSize(170, 40)
        self.checkallpetbutton.setText("查看所有宠物")
        self.checkallpetbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.checkallpetbutton.clicked.connect(self.petView)
        self.feedbackbutton = QPushButton()
        self.feedbackbutton.setFixedSize(170, 40)
        self.feedbackbutton.setText("反 馈  信 息")
        self.feedbackbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.feedbackbutton.clicked.connect(self.feedback)
        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.checkallpetbutton)
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.feedbackbutton)
        self.h3box.addStretch(1)

        self.releasepetbutton = QPushButton()
        self.releasepetbutton.setFixedSize(170,40)
        self.releasepetbutton.setText("发 布  招 领")
        self.releasepetbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.releasepetbutton.clicked.connect(self.releasePet)
        self.releasehistorybutton = QPushButton()
        self.releasehistorybutton.setFixedSize(170, 40)
        self.releasehistorybutton.setText("我发布的宠物")
        self.releasehistorybutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.releasehistorybutton.clicked.connect(self.releaseHistory)
        self.h4box = QHBoxLayout()
        self.h4box.addStretch(1)
        self.h4box.addWidget(self.releasepetbutton)
        self.h4box.addStretch(1)
        self.h4box.addWidget(self.releasehistorybutton)
        self.h4box.addStretch(1)

        self.adoptpetbutton = QPushButton()
        self.adoptpetbutton.setFixedSize(170, 40)
        self.adoptpetbutton.setText("领 养  宠 物")
        self.adoptpetbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.adoptpetbutton.clicked.connect(self.adoptPet)
        self.adopthistorybutton = QPushButton()
        self.adopthistorybutton.setFixedSize(170, 40)
        self.adopthistorybutton.setText("我的领养历史")
        self.adopthistorybutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.adopthistorybutton.clicked.connect(self.adoptHistory)
        self.h5box = QHBoxLayout()
        self.h5box.addStretch(1)
        self.h5box.addWidget(self.adoptpetbutton)
        self.h5box.addStretch(1)
        self.h5box.addWidget(self.adopthistorybutton)
        self.h5box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h4box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h5box)
        self.vbox.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)

    def releasePet(self):
        releasepetdialog = ReleasePetDialog(self.UserId)
        releasepetdialog.show()
        releasepetdialog.exec_()

    def petView(self):
        petviewdialog = PetViewer()
        petviewdialog.show()
        petviewdialog.exec_()

    def feedback(self):
        feedbackdialog = FeedBackDialog(self.UserId)
        feedbackdialog.show()
        feedbackdialog.exec_()

    def adoptPet(self):
        adoptpetdialog = ApplyAdoptDialog(self.UserId)
        adoptpetdialog.show()
        adoptpetdialog.exec_()

    def releaseHistory(self):
        releasehistorydialog = ReleasePetHistory(self.UserId)
        releasehistorydialog.show()
        releasehistorydialog.exec_()

    def adoptHistory(self):
        adopthistorydialog = AdoptPetHistory(self.UserId)
        adopthistorydialog.show()
        adopthistorydialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    userhomeWindow = UserHome('csxuhuan')
    userhomeWindow.show()
    sys.exit(app.exec_())

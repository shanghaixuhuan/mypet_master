import sys
from PyQt5.QtWidgets import (QWidget,QApplication,QHBoxLayout,QVBoxLayout,
                             QPushButton,QLabel)
from PyQt5.QtGui import QIcon,QFont
import qdarkstyle
from PetViewer import PetViewer
from UserManage import UserManageDialog
from ReceiveFeedback import ReceiveFeedbackDialog
from CheckAdopt import CheckAdoptDialog


class AdminHome(QWidget):
    def __init__(self,adminid):
        super(AdminHome,self).__init__()
        self.resize(900,600)
        self.adminid = adminid
        self.setWindowTitle('myPet——管理员界面')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.initUI()

    def initUI(self):
        self.whelcomelabel = QLabel()
        self.whelcomelabel.setText(" 欢迎登录\n管理员界面")
        self.whelcomelabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.usermanagebutton = QPushButton()
        self.usermanagebutton.setFixedSize(120,40)
        self.usermanagebutton.setText("用户管理")
        self.usermanagebutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.usermanagebutton.clicked.connect(self.usermanageClicked)
        self.receivefeedbackbutton = QPushButton()
        self.receivefeedbackbutton.setFixedSize(120, 40)
        self.receivefeedbackbutton.setText("用户反馈")
        self.receivefeedbackbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.receivefeedbackbutton.clicked.connect(self.receivefeedbackClicked)
        self.checkadoptbutton = QPushButton()
        self.checkadoptbutton.setFixedSize(120, 40)
        self.checkadoptbutton.setText("审核领养")
        self.checkadoptbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.checkadoptbutton.clicked.connect(self.checkadoptClicked)

        self.petviewer = PetViewer()

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.whelcomelabel)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.usermanagebutton)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.receivefeedbackbutton)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.checkadoptbutton)
        self.vbox.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox)
        self.hbox.addWidget(self.petviewer)
        self.setLayout(self.hbox)

    def usermanageClicked(self):
        usermanageDialog = UserManageDialog(self.adminid)
        usermanageDialog.show()
        usermanageDialog.exec_()

    def receivefeedbackClicked(self):
        receivefeedbackDialog = ReceiveFeedbackDialog()
        receivefeedbackDialog.show()
        receivefeedbackDialog.exec_()

    def checkadoptClicked(self):
        checkadoptdialog = CheckAdoptDialog(self.adminid)
        checkadoptdialog.show()
        checkadoptdialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    adminhomeWindow = AdminHome('admin')
    adminhomeWindow.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QAction
from PyQt5.QtGui import QIcon,QFont
from SignIn import SignInWidget
from SignUp import SignUpWidget
from About import AboutDialog
from ChangePsw import ChangePswDialog
from AdminHome import AdminHome
from UserHome import UserHome
import qdarkstyle


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('myPet——欢迎使用宠物招领系统')
        self.setWindowIcon(QIcon('./images/icon.png'))

        self.widget = SignInWidget()
        self.setCentralWidget(self.widget)

        menubar = self.menuBar()
        menubar.setFont(QFont("苏新诗柳楷繁", 15))
        self.menu = menubar.addMenu('菜单栏')
        self.menu.setFont(QFont("苏新诗柳楷繁", 15))
        self.signupaction = QAction("注    册",self)
        self.signupaction.setShortcut('Ctrl+U')
        self.signinaction = QAction('登    录',self)
        self.signinaction.setShortcut('Ctrl+I')
        self.changepswaction = QAction("修改密码", self)
        self.changepswaction.setShortcut('Ctrl+C')
        self.aboutaction = QAction("关    于",self)
        self.aboutaction.setShortcut('Ctrl+A')
        self.quitsigninaction = QAction("退出登录",self)
        self.quitsigninaction.setShortcut('Ctrl+T')
        self.quitaction = QAction("退    出", self)
        self.quitaction.setShortcut('Ctrl+Q')
        self.menu.addAction(self.signupaction)
        self.menu.addAction(self.signinaction)
        self.menu.addAction(self.changepswaction)
        self.menu.addAction(self.aboutaction)
        self.menu.addAction(self.quitsigninaction)
        self.menu.addAction(self.quitaction)
        self.signupaction.setEnabled(True)
        self.changepswaction.setEnabled(True)
        self.signinaction.setEnabled(False)
        self.quitsigninaction.setEnabled(False)

        self.widget.is_admin_signal[str].connect(self.adminSignIn)
        self.widget.is_user_signal[str].connect(self.userSignIn)
        self.menu.triggered[QAction].connect(self.menuTriggered)

    def menuTriggered(self,q):
        if(q.text() == "注    册"):
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            self.signupaction.setEnabled(False)
            self.changepswaction.setEnabled(True)
            self.signinaction.setEnabled(True)
            self.quitsigninaction.setEnabled(False)
        if(q.text() == "登    录"):
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal[str].connect(self.adminSignIn)
            self.widget.is_user_signal[str].connect(self.userSignIn)
            self.signupaction.setEnabled(True)
            self.changepswaction.setEnabled(True)
            self.signinaction.setEnabled(False)
            self.quitsigninaction.setEnabled(False)
        if(q.text() == "退出登录"):
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal[str].connect(self.adminSignIn)
            self.widget.is_user_signal[str].connect(self.userSignIn)
            self.signupaction.setEnabled(True)
            self.changepswaction.setEnabled(True)
            self.signinaction.setEnabled(False)
            self.quitsigninaction.setEnabled(False)
        if (q.text() == "修改密码"):
            changepswDialog = ChangePswDialog()
            changepswDialog.show()
            changepswDialog.exec_()
        if(q.text() == "关    于"):
            aboutDialog = AboutDialog()
            aboutDialog.show()
            aboutDialog.exec_()
        if(q.text() == "退    出"):
            qApp = QApplication.instance()
            qApp.quit()
        return

    def adminSignIn(self,userId):
        self.widget = AdminHome(userId)
        self.setCentralWidget(self.widget)
        self.signupaction.setEnabled(False)
        self.changepswaction.setEnabled(False)
        self.signinaction.setEnabled(False)
        self.quitsigninaction.setEnabled(True)

    def userSignIn(self,userId):
        self.widget = UserHome(userId)
        self.setCentralWidget(self.widget)
        self.signupaction.setEnabled(False)
        self.changepswaction.setEnabled(False)
        self.signinaction.setEnabled(False)
        self.quitsigninaction.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
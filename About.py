import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont


class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(700,500)
        self.setWindowTitle("myPet——关于")
        self.setWindowIcon(QIcon("./images/icon.png"))

        # 标题标签组件
        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('./images/title.png')
        self.titlelabel.setPixmap(self.titleimage)

        self.textlabel = QLabel(self)
        self.textlabel.setText("    本宠物找零系统为华东理工大学2016级数据库\n"
                               "原理课程课程设计，实现对遗失宠物、宠物招领发布、\n"
                               "宠物收养、查看招领信息等进行统一管理。")
        self.textlabel.setFont(QFont("苏新诗柳楷繁",15))

        self.toolslabel = QLabel(self)
        self.toolslabel.setText("版本号：2 . 0 . 0\n"
                                "库：PyQt5  数据库：sqlite")
        self.toolslabel.setFont(QFont("苏新诗柳楷繁", 15))

        self.memberslabel = QLabel(self)
        self.memberslabel.setText("小组成员：计162 徐涣 10161762\n"
                                  "         计162 盛泽宇 10161768")
        self.memberslabel.setFont(QFont("苏新诗柳楷繁", 15))

        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.textlabel)
        self.h2box.addStretch(1)

        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.toolslabel)
        self.h3box.addStretch(1)

        self.h4box = QHBoxLayout()
        self.h4box.addStretch(1)
        self.h4box.addWidget(self.memberslabel)
        self.h4box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h4box)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    aboutWindow = AboutDialog()
    aboutWindow.show()
    sys.exit(app.exec_())
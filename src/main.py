import os
import stat
import sys
from pathlib import Path

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel

from permissions import FilePerm

target_db = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "somesqlite.db")
home_dir = os.path.expanduser("~")
qtCreatorFile = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "ui", "mainwindow.ui")
UiDesignWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class PerfmWindow(QMainWindow, UiDesignWindow):
    def __init__(self):
        super(PerfmWindow, self).__init__()
        self.setupUi(self)

        self.model = QFileSystemModel()
        homedir = os.environ['HOME']
        self.model.setRootPath(homedir)
        self.treeView.setModel(self.model)

        self.treeView.setAnimated(False)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)
        self.treeView.clicked.connect(self.open_file_information)

    def get_file_stuffs(self, qfile):
        self.file_name_info.setText(QFileInfo.canonicalFilePath(qfile))
        self.file_size_info.setText(QFileInfo.size(qfile))
        self.file_changed_info.setText(QFileInfo.lastModified(qfile))

    def open_file_information(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        # os.startfile(file_path)
        qfile = QFileInfo(file_path)
        file_modified = qfile.lastModified().toString()
        self.file_name_info.setText(qfile.canonicalFilePath())
        self.file_size_info.setText(str(qfile.size()))
        self.file_changed_info.setText(str(file_modified))
        perms = FilePerm(file_path)
        user_perms = perms.permissions['user']
        group_perms = perms.permissions['group']
        other_perms = perms.permissions['other']
        self.permissions_info_user.setText(''.join(user_perms))
        self.permissions_info_group.setText(''.join(group_perms))
        self.permissions_info_other.setText(''.join(other_perms))
        (perms.__dict__.keys())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PerfmWindow()
    window.show()
    sys.exit(app.exec_())


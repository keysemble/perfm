import os
import stat
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel
from PyQt5.QtCore import QFileInfo

from permissions import FilePerm

home_dir = os.path.expanduser("~")
qt_creator_file = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "ui", "design_window.ui")

DesignWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class PerfmWindow(QMainWindow, DesignWindow):
    def __init__(self):
        super(PerfmWindow, self).__init__()
        self.setupUi(self)

        self.model = QFileSystemModel()
        self.model.setRootPath(os.environ['HOME'])
        self.tree_view.setModel(self.model)

        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.clicked.connect(self.open_file_information)

    def open_file_information(self):
        file_path = self.model.filePath(self.tree_view.currentIndex())
        qfile = QFileInfo(file_path)
        file_modified = qfile.lastModified().toString()
        self.file_name_value.setText(qfile.canonicalFilePath())
        self.file_size_value.setText(str(qfile.size()))
        self.last_modified_value.setText(str(file_modified))
        fileperm = FilePerm(file_path)
        r, w, x = fileperm.access_bits('user')
        self.user_read_checkbox.setChecked(r)
        self.user_write_checkbox.setChecked(w)
        self.user_execute_checkbox.setChecked(x)
        r, w, x = fileperm.access_bits('group')
        self.group_read_checkbox.setChecked(r)
        self.group_write_checkbox.setChecked(w)
        self.group_execute_checkbox.setChecked(x)
        r, w, x = fileperm.access_bits('other')
        self.other_read_checkbox.setChecked(r)
        self.other_write_checkbox.setChecked(w)
        self.other_execute_checkbox.setChecked(x)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PerfmWindow()
    window.show()
    sys.exit(app.exec_())


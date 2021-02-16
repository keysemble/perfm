import os
import stat
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QMessageBox, QStatusBar
from PyQt5.QtCore import QFileInfo

from permissions import FilePerm
from humanbytes import HumanBytes

home_dir = os.path.expanduser('~')
qt_creator_file = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'design_window.ui')
app_icon = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'icons', 'Icon.ico')
DesignWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class PerfmWindow(QMainWindow, DesignWindow):
    def __init__(self):
        super(PerfmWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Perfm Filemanager')
        self.setWindowIcon(QtGui.QIcon(app_icon))
        self.status_bar = self.statusBar()
        self.file_path = ''

        self.model = QFileSystemModel()
        self.model.setRootPath(os.environ['HOME'])
        self.tree_view.setModel(self.model)

        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.clicked.connect(self.open_file_information)
        self.tree_view.resizeColumnToContents(0)

        self.apply_push_button.clicked.connect(self.apply_checkbox_changes)

    def open_file_information(self):
        self.tree_view.resizeColumnToContents(0)
        self.file_path = self.model.filePath(self.tree_view.currentIndex())
        qfile = QFileInfo(self.file_path)
        file_modified = qfile.lastModified().toString()
        self.file_name_value.setText(qfile.canonicalFilePath())
        self.file_size_value.setText(str(HumanBytes.format(qfile.size(), precision=2)))
        self.last_modified_value.setText(str(file_modified))
        fileperm = FilePerm(self.file_path)
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

    def apply_checkbox_changes(self):
        self.tree_view.resizeColumnToContents(0)
        file_path = self.model.filePath(self.tree_view.currentIndex())
        fileperm = FilePerm(file_path)
        settings = {
            "user": [
                self.user_read_checkbox.isChecked(),
                self.user_write_checkbox.isChecked(),
                self.user_execute_checkbox.isChecked(),
            ],
            "group": [
                self.group_read_checkbox.isChecked(),
                self.group_write_checkbox.isChecked(),
                self.group_execute_checkbox.isChecked(),
            ],
            "other": [
                self.other_read_checkbox.isChecked(),
                self.other_write_checkbox.isChecked(),
                self.other_execute_checkbox.isChecked(),
            ],
        }
        fileperm.update_bitwise(settings)
        message_text = f"Applied Permissions to {self.file_path}"
        self.open_file_information()
        self.status_bar.showMessage(message_text, 10000)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PerfmWindow()
    window.show()
    sys.exit(app.exec_())

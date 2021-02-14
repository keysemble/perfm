# from fbs_runtime.application_context import is_frozen
# from fbs_runtime.excepthook.sentry import SentryExceptionHandler
import os
import os.path
import stat
from pathlib import Path
import sys
# import requests
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from fbs_runtime.application_context.PyQt5 import ApplicationContext, \
    cached_property

# example of dynamically loading sqlite from cwd of installer

target_db = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "somesqlite.db")

home_dir = os.path.expanduser("~")
somefile = Path(os.path.join("~/.bashrc"))


def octal_permission_digit(rwx):
    digit = 0
    if rwx[0] == 'r':
        digit += 4
    if rwx[1] == 'w':
        digit += 2
    if rwx[2] == 'x':
        digit += 1
    return digit


class FilePerm:
    def __init__(self, filepath):
        filemode = stat.filemode(os.stat(filepath).st_mode)
        permission_group = [filemode[-9:][i:i + 3] for i in range(0, len(filemode[-9:]), 3)]
        self.filepath = filepath
        self.permissions = dict(zip(['user', 'group', 'other'], [list(p) for p in permission_group]))

    def get_mode(self):
        octal_digits = [octal_permission_digit(p) for p in self.permissions.values()]
        mode = 0
        for shift, octal in enumerate(octal_digits[::-1]):
            mode += octal << (shift * 3)
        return mode

    def update(self, access, read=None, write=None, execute=None):
        if access in self.permissions.keys():
            perm = self.permissions[access]
            if read is not None:
                if read:
                    perm[0] = 'r'
                else:
                    perm[0] = '-'
            if write is not None:
                if write:
                    perm[1] = 'w'
                else:
                    perm[1] = '-'
            if execute is not None:
                if execute:
                    perm[2] = 'x'
                else:
                    perm[2] = '-'
            os.chmod(self.filepath, self.get_mode())


class AppContext(ApplicationContext):
    def run(self):
        version = self.build_settings['version']
        QApplication.setApplicationName("Perfm")
        QApplication.setOrganizationName("Perfm")
        QApplication.setOrganizationDomain("Perfm.perfm")
        current_version = version
        self.main_window.setWindowTitle("Perfm v" + version)
        # # current release version url
        # current_release_url = 'https:///Perfm.com/current_release.txt'
        #
        # def versiontuple(v):
        #     return tuple(map(int, (v.split("."))))
        #
        # try:
        #     # Parse current release version from url
        #     response = requests.get(current_release_url)
        #     current_release = response.text
        #
        #     print('Current Version: ' + current_version)
        #     print('Current Release: ' + current_release)
        #     # Compare versions
        #     if versiontuple(current_release) > versiontuple(current_version):
        #         print('New Update Available: ' + current_release)
        #         self.main_window.setWindowTitle(
        #             "Perfm v" + version + '| New Update Available: ' + current_release)
        #         self.main_window.set(
        #             "Perfm v" + version + '| New Update Available: ' + current_release)
        #         update_available = True
        #     else:
        #         update_available = False
        #     print('Update Available:' + str(update_available))
        # except:
        #
        #     pass

        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MainWindow(self)

    QApplication.setStyle("Fusion")
    #
    # # Now use a palette to switch to dark colors:
    QApplication.setStyle("Fusion")
    #
    # # Now use a palette to switch to dark colors:
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    QApplication.setPalette(dark_palette)

    # @cached_property
    # def app_db(self):
    #     global target_db_path
    #     target_db_path = self.get_resource('somesqlite.db')
    #     return QSqlDatabase(self.get_resource('somesqlite.db'))

    # @cached_property
    # def app_style(self):
    #     # global stylesheet
    #     return QFile(self.get_resource('mystylesheet.css'))


qtCreatorFile = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "ui",
                             "mainwindow.ui")  # Type your file path
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.ctx = ctx
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        self.setupUi(self)
        # self.show()

        self.model = QFileSystemModel()
        homedir = os.environ['HOME']
        self.model.setRootPath(homedir)
        self.treeView.setModel(self.model)

        self.treeView.setAnimated(False)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)
        self.treeView.clicked.connect(self.open_file_information)

    def get_file_stuffs(self, file):
        self.file_name_info.setText(QFileInfo.canonicalFilePath(file))
        self.file_size_info.setText(QFileInfo.size(file))
        self.file_changed_info.setText(QFileInfo.lastModified(file))

    def open_file_information(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        # os.startfile(file_path)
        file = QFileInfo(file_path)
        file_modified = file.lastModified().toString()
        self.file_name_info.setText(file.canonicalFilePath())
        self.file_size_info.setText(str(file.size()))
        self.file_changed_info.setText(str(file_modified))
        perms = FilePerm(file_path)
        user_perms = perms.permissions['user']
        group_perms = perms.permissions['group']
        other_perms = perms.permissions['other']
        self.permissions_info_user.setText(''.join(user_perms))
        self.permissions_info_group.setText(''.join(group_perms))
        self.permissions_info_other.setText(''.join(other_perms))
        print(vars(perms))
        (perms.__dict__.keys())
        # att_perms = [attr for attr in dir(perms()) if not callable(getattr(perms(), attr)) and not attr.startswith("__")]
        #print(att_perms)
        print(str(perms.get_mode()))
        print(QFile(file_path))
        print(file.permissions())
        print(str(QFile(file_path)))
        print()
        print('File: %s' % file.filePath())
        print('')
        print('Qt Writable: %s' % file.isWritable())
        print('Qt Permission: %s' % bool(file.permissions() & QFile.WriteUser))
        print('Py Writable: %s' % os.access(file_path, os.W_OK))
        print('Py Permission: %s' % bool(os.stat(file_path).st_mode & stat.S_IWUSR))


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)

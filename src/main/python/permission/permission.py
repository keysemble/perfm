import stat
import os


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

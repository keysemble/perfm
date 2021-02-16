import stat
import os
from enum import Enum
from collections import namedtuple


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
        permissions = [filemode[-9:][i:i + 3] for i in range(0, len(filemode[-9:]), 3)]
        self.filepath = filepath
        self.access_dict = dict(zip(['user', 'group', 'other'], [list(perm) for perm in permissions]))

    def mode(self):
        octal_digits = [octal_permission_digit(p) for p in self.access_dict.values()]
        mode = 0
        for shift, octal in enumerate(octal_digits[::-1]):
            mode += octal << (shift * 3)
        return mode

    def access_bits(self, access):
        if access in self.access_dict.keys():
            r, w, x = self.access_dict[access]
            return [r == 'r', w == 'w', x == 'x']

    def update_bitwise(self, settings):
        def perm_list(read=False, write=False, execute=False):
            pl = ['-', '-', '-']
            if read:
                pl[0] = 'r'
            if write:
                pl[1] = 'w'
            if execute:
                pl[2] = 'x'
            return pl

        self.access_dict = dict([(access, perm_list(read=r, write=w, execute=x)) for access, [r, w, x] in settings.items()])
        os.chmod(self.filepath, self.get_mode())

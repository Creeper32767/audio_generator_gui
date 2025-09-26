import winreg
from os.path import expandvars, abspath


def get_desktop_location():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    )

    path, _ = winreg.QueryValueEx(key, "Desktop")
    return abspath(expandvars(path))

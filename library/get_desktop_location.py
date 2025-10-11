from os.path import join, expanduser


def get_desktop_location() -> str:
    return join(expanduser("~"), "Desktop")


if __name__ == "__main__":
    print(get_desktop_location())

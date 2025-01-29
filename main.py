import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition, setTheme, Theme

from library import read_json, International, search
from interfaces import InfoWindow, GenerationWindow, SettingsWindow

# setting name and version
__version__ = "1.4"
config = read_json("./config.json")
Translator = International(config["locale"], "./lang/")


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{Translator.get_text('application.name')} - {__version__}")
        self.setWindowIcon(QIcon("./assets/person_voice.svg"))
        self.resize(1000, 800)
        theme = search(config, "theme")
        if theme == "AUTO":
            setTheme(Theme.AUTO)
        elif theme == "DARK":
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.LIGHT)

        # add sub-windows
        ui_generation = GenerationWindow(Translator, parent=self)
        self.addSubInterface(
            ui_generation,
            icon=FluentIcon.VOLUME,
            text=Translator.get_text("application.ui.generation")
        )

        ui_settings = SettingsWindow(Translator, current_choice=config["theme"])
        self.addSubInterface(
            ui_settings,
            icon=FluentIcon.SETTING,
            text=Translator.get_text("application.ui.settings")
        )

        ui_about = InfoWindow(Translator, version=__version__, parent=self)
        self.addSubInterface(
            ui_about,
            icon=FluentIcon.INFO,
            text=Translator.get_text("application.ui.about"),
            position=NavigationItemPosition.BOTTOM,)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())

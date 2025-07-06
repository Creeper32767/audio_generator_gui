from sys import argv, exit
from PySide6.QtCore import QSize, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition, setTheme, Theme, isDarkTheme, SplashScreen
from qframelesswindow import StandardTitleBar

from library import BaseJsonOperator, International, TTSWorker
from interfaces import InfoWindow, GenerationWindow, SettingsWindow

# setting name and version
__version__ = "1.7.0"
config = BaseJsonOperator("./config.json")
voice_index = BaseJsonOperator("./VOICE_INDEX")
Translator = International(config.search("application.locale", "zh-cn"), "./lang/")


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{Translator.get_text('application.name')} - {__version__}")
        self.tts_generator = TTSWorker(
            (Translator.get_text("ui.generation.choose_locale"),
             Translator.get_text("ui.generation.choose_gender"),
             Translator.get_text("ui.generation.choose_voice"))
        )
        self.setup_splash_window()

    def setup_splash_window(self):
        self.setWindowIcon(QIcon(f"./assets/person_voice.ico"))
        self.resize(500, 300)
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(102, 102))
        title_bar = StandardTitleBar(self.splash_screen)
        title_bar.setIcon(self.windowIcon())
        title_bar.setTitle(self.windowTitle())
        self.splash_screen.setTitleBar(title_bar)

        screen = QApplication.primaryScreen().availableGeometry().center()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen)
        self.move(geometry.topLeft())

        # defining activity
        title_bar.setTitle(self.windowTitle() + " - Loading Voice Indexes...")
        self.fetch_voice_list()

    def fetch_voice_list(self):
        if config.search("application.auto_download_index", False) or voice_index.json_content == dict():
            thread = QThread(self)
            self.tts_generator.moveToThread(thread)
            thread.started.connect(self.tts_generator.starting_fetching)
            self.tts_generator.finished.connect(self.splash_screen.finish)
            self.tts_generator.finished.connect(thread.quit)
            self.tts_generator.finished.connect(self.setup_ui)
            self.tts_generator.error.connect(self.show_error_message)
            thread.start()
            thread.wait()
        else:
            self.tts_generator.edit_voice_list(voice_index.json_content)
            self.splash_screen.finish()
            self.setup_ui()

    @staticmethod
    def show_error_message(message: str):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setWindowTitle("Error")
        error_message.setText(Translator.get_text("ui.generation.message.failed").format(message))
        error_message.setStandardButtons(QMessageBox.Ok)
        error_message.exec()
        exit("ERROR")

    def setup_ui(self):
        self.hide()
        voice_index.json_content = self.tts_generator.indexes_common
        voice_index.write_json()
        theme = [Theme.AUTO, Theme.LIGHT, Theme.DARK][config.search("application.theme", 0)]
        setTheme(theme)
        theme = "DARK" if isDarkTheme() else "LIGHT"
        self.setWindowIcon(QIcon(f"./assets/{theme}/person_voice.svg"))
        self.resize(800, 800)

        screen = QApplication.primaryScreen().availableGeometry().center()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen)
        self.move(geometry.topLeft())

        # add sub-windows
        ui_generation = GenerationWindow(Translator, config, theme, self.tts_generator, parent=self)
        self.addSubInterface(
            ui_generation,
            icon=FluentIcon.VOLUME,
            text=Translator.get_text("application.ui.generation")
        )

        ui_settings = SettingsWindow(Translator, config, theme, parent=self)
        self.addSubInterface(
            ui_settings,
            icon=FluentIcon.SETTING,
            text=Translator.get_text("application.ui.settings")
        )
        ui_settings.restartRequested.connect(self.handle_restart)

        ui_about = InfoWindow(Translator, __version__, parent=self)
        self.addSubInterface(
            ui_about,
            icon=FluentIcon.INFO,
            text=Translator.get_text("application.ui.about"),
            position=NavigationItemPosition.BOTTOM
        )
        self.show()

    @staticmethod
    def handle_restart():
        from sys import executable, argv
        from os import execl
        QApplication.quit()
        execl(executable, executable, *argv)


if __name__ == '__main__':
    app = QApplication(argv)
    w = Window()
    w.show()
    exit(app.exec())

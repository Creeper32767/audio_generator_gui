import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition, setTheme, Theme

from library import read_json, International, search
from interfaces import InfoWindow, GenerationWindow, SettingsWindow

# setting name and version
__version__ = "1.3"
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
        ui_generation = GenerationWindow(
            page_text=(Translator.get_text("ui_generation.title"),
                       Translator.get_text("ui_generation.placeholder"),
                       Translator.get_text("ui_generation.generate"),
                       Translator.get_text("ui_generation.choice_title"),
                       Translator.get_text("ui_generation.choose_locale_title"),
                       Translator.get_text("ui_generation.choose_locale_content"),
                       Translator.get_text("ui_generation.choose_gender_title"),
                       Translator.get_text("ui_generation.choose_gender_content"),
                       Translator.get_text("ui_generation.choose_voice_title"),
                       Translator.get_text("ui_generation.choose_voice_content"),
                       Translator.get_text("ui_generation.enter_rate_title"),
                       Translator.get_text("ui_generation.enter_rate_content"),
                       Translator.get_text("ui_generation.enter_volume_title"),
                       Translator.get_text("ui_generation.enter_volume_content"),
                       Translator.get_text("ui_generation.choose_folder_title"),
                       Translator.get_text("ui_generation.choose_folder_content"),
                       Translator.get_text("ui_generation.show_path")
                       ),
            message_text=(Translator.get_text("ui_generation.message.success"),
                          Translator.get_text("ui_generation.message.failed")
                          ),
            voice_choice_message=(Translator.get_text("ui_generation.choose_locale"),
                                  Translator.get_text("ui_generation.choose_gender"),
                                  Translator.get_text("ui_generation.choose_voice")
                                  ),
            parent=self)
        self.addSubInterface(
            ui_generation,
            icon=FluentIcon.VOLUME,
            text=Translator.get_text("application.ui.generation")
        )

        ui_settings = SettingsWindow(
            page_text=(Translator.get_text("application.ui.settings"),
                       Translator.get_text("ui_settings.choose_language_title"),
                       Translator.get_text("ui_settings.choose_language_content"),
                       Translator.get_text("ui_settings.choose_theme_title"),
                       Translator.get_text("ui_settings.choose_theme_content"),
                       Translator.get_text("ui_settings.restart")

            ),
            current_choice=(Translator.get_supported_languages(),
                            Translator.locale,
                            ["LIGHT", "DARK", "AUTO"],
                            config["theme"]
            )

        )
        self.addSubInterface(
            ui_settings,
            icon=FluentIcon.SETTING,
            text=Translator.get_text("application.ui.settings")
        )

        ui_about = InfoWindow(
            view_it_on_github=Translator.get_text('ui_about.button_text'),
            version=__version__,
            dev_info=(Translator.get_text('ui_about.developer.info'), Translator.get_text('ui_about.developer.content')),
            parent=self)
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

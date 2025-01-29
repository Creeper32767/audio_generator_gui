from os import execv
from sys import executable, argv
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qfluentwidgets import GroupHeaderCardWidget, ComboBox, PushButton

from library import edit, International


class SettingsWindow(QMainWindow):
    def __init__(self, translator: International, current_choice: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsWindow")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.vertical_layout = QVBoxLayout()
        central_widget.setLayout(self.vertical_layout)

        self.settngs_card = GroupHeaderCardWidget(parent=self)
        self.settngs_card.setTitle(translator.get_text("application.ui.settings"))
        # language
        self.languages = ComboBox()
        self.languages.setMaxVisibleItems(10)
        self.languages.addItems(translator.get_supported_languages())
        self.languages.setCurrentText(translator.locale)
        self.languages.currentTextChanged.connect(self.selection_changed)
        # theme
        self.theme = ComboBox()
        self.theme.addItems(translator.get_text("ui.settings.choose_theme_choices"))
        self.theme.setCurrentText(current_choice)
        self.theme.currentTextChanged.connect(self.selection_changed)
        # join in layout
        self.settngs_card.addGroup("./assets/language.svg",
                                   translator.get_text("ui_settings.choose_language_title"),
                                   translator.get_text("ui_settings.choose_language_content"),
                                   self.languages)
        self.settngs_card.addGroup("./assets/theme.svg",
                                   translator.get_text("ui_settings.choose_theme_title"),
                                   translator.get_text("ui_settings.choose_theme_title"),
                                   self.theme)
        self.vertical_layout.addWidget(self.settngs_card)

        # Add a vertical spacer
        self.vertical_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_layout.addItem(self.vertical_spacer)

        # restart button
        self.restart_button = PushButton(translator.get_text("ui_settings.restart"))
        self.restart_button.clicked.connect(self.restart)

    def selection_changed(self):
        if self.restart_button is not None:
            self.vertical_layout.addWidget(self.restart_button)
        edit("./config.json", "locale", self.languages.currentText())
        edit("./config.json", "theme", self.theme.currentText())

    def restart(self):
        execv(executable, [executable] + argv)

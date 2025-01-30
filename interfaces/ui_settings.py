from os import execv
from sys import executable, argv
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qfluentwidgets import GroupHeaderCardWidget, ComboBox, PushButton

from library import International, BaseJsonOperator


class SettingsWindow(QMainWindow):
    def __init__(self, translator: International, config: BaseJsonOperator, theme, parent=None):
        super().__init__(parent=parent)
        self.config = config
        self.theme = theme
        self.setObjectName("SettingsWindow")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.vertical_layout = QVBoxLayout()
        central_widget.setLayout(self.vertical_layout)

        self.settngs_card = GroupHeaderCardWidget(parent=self)
        self.settngs_card.setTitle(translator.get_text("application.ui.settings"))
        # language
        self.languages_combo_box = ComboBox()
        self.languages_combo_box.setMaxVisibleItems(10)
        self.languages_combo_box.addItems(translator.get_supported_languages())
        self.languages_combo_box.setCurrentText(translator.locale)
        self.languages_combo_box.currentTextChanged.connect(self.selection_changed)
        # theme
        self.theme_combo_box = ComboBox()
        self.theme_combo_box.addItems(translator.get_text("ui.settings.choose_theme_choices"))
        self.theme_combo_box.setCurrentText(self.config.search("theme", "LIGHT"))
        self.theme_combo_box.currentTextChanged.connect(self.selection_changed)
        # join in layout
        self.settngs_card.addGroup(f"./assets/{self.theme}/language.svg",
                                   translator.get_text("ui_settings.choose_language_title"),
                                   translator.get_text("ui_settings.choose_language_content"),
                                   self.languages_combo_box)
        self.settngs_card.addGroup(f"./assets/{self.theme}/theme.svg",
                                   translator.get_text("ui_settings.choose_theme_title"),
                                   translator.get_text("ui_settings.choose_theme_title"),
                                   self.theme_combo_box)
        self.vertical_layout.addWidget(self.settngs_card)

        # Add a vertical spacer
        self.vertical_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_layout.addItem(self.vertical_spacer)

        # restart button
        self.restart_button = PushButton(translator.get_text("ui_settings.restart"))
        self.restart_button.clicked.connect(lambda : execv(executable, [f'"{executable}"'] + argv))

    def selection_changed(self):
        if self.restart_button is not None:
            self.vertical_layout.addWidget(self.restart_button)
        self.config.edit("locale", self.languages_combo_box.currentText())
        self.config.edit("theme", self.theme_combo_box.currentText())

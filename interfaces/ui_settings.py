from os import execv
from sys import executable, argv
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qfluentwidgets import GroupHeaderCardWidget, ComboBox, PushButton

from library import edit


class SettingsWindow(QMainWindow):
    def __init__(self, page_text: tuple, current_choice: tuple, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsWindow")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.vertical_layout = QVBoxLayout()
        central_widget.setLayout(self.vertical_layout)

        self.settngs_card = GroupHeaderCardWidget(parent=self)
        self.settngs_card.setTitle(page_text[0])
        # language
        self.languages = ComboBox()
        self.languages.setMaxVisibleItems(10)
        self.languages.addItems(current_choice[0])
        self.languages.setCurrentText(current_choice[1])
        self.languages.currentTextChanged.connect(self.selection_changed)
        # theme
        self.theme = ComboBox()
        self.theme.addItems(current_choice[2])
        self.theme.setCurrentText(current_choice[3])
        self.theme.currentTextChanged.connect(self.selection_changed)
        # join in layout
        self.settngs_card.addGroup("./assets/language.svg", page_text[1], page_text[2], self.languages)
        self.settngs_card.addGroup("./assets/theme.svg", page_text[3], page_text[4], self.theme)
        self.vertical_layout.addWidget(self.settngs_card)

        # Add a vertical spacer
        self.vertical_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_layout.addItem(self.vertical_spacer)

        # restart button
        self.restart_button = PushButton(page_text[5])
        self.restart_button.clicked.connect(self.restart)

    def selection_changed(self):
        if self.restart_button is not None:
            self.vertical_layout.addWidget(self.restart_button)
        edit("./config.json", "locale", self.languages.currentText())
        edit("./config.json", "theme", self.theme.currentText())

    def restart(self):
        execv(executable, [executable] + argv)

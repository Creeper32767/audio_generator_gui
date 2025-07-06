from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from qfluentwidgets import GroupHeaderCardWidget, ComboBox, PushButton, SwitchButton, FluentIcon

from library import International, BaseJsonOperator


class SettingsWindow(QMainWindow):
    restartRequested = Signal()

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
        self.theme_combo_box.addItems(translator.get_text("ui.settings.choose_theme.choices"))
        self.theme_combo_box.setCurrentIndex(self.config.search("application.theme", 0))
        self.theme_combo_box.currentTextChanged.connect(self.selection_changed)
        # download voice index
        self.download_index_checkbox = SwitchButton()
        self.download_index_checkbox.setChecked(config.search("application.auto_download_index"))
        self.download_index_checkbox.checkedChanged.connect(self.selection_changed)
        self.download_index_checkbox.setOnText(translator.get_text("ui.settings.autodownload.texts")[0])
        self.download_index_checkbox.setOffText(translator.get_text("ui.settings.autodownload.texts")[1])
        # join in layout
        self.settngs_card.addGroup(f"./assets/{self.theme}/language.svg",
                                   translator.get_text("ui.settings.choose_language.title"),
                                   translator.get_text("ui.settings.choose_language.content"),
                                   self.languages_combo_box)
        self.settngs_card.addGroup(f"./assets/{self.theme}/theme.svg",
                                   translator.get_text("ui.settings.choose_theme.title"),
                                   translator.get_text("ui.settings.choose_theme.content"),
                                   self.theme_combo_box)
        self.settngs_card.addGroup(FluentIcon.DOWNLOAD,
                                   translator.get_text("ui.settings.autodownload.title"),
                                   translator.get_text("ui.settings.autodownload.content"),
                                   self.download_index_checkbox)
        self.vertical_layout.addWidget(self.settngs_card)

        # Add a vertical spacer
        self.vertical_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_layout.addItem(self.vertical_spacer)

        # restart button
        self.restart_button = PushButton(translator.get_text("ui.settings.restart"))
        self.restart_button.clicked.connect(self.restart)

    def selection_changed(self):
        if self.restart_button is not None:
            self.vertical_layout.addWidget(self.restart_button)
        self.config.edit("application.locale", self.languages_combo_box.currentText())
        self.config.edit("application.theme", self.theme_combo_box.currentIndex())
        self.config.edit("application.auto_download_index", self.download_index_checkbox.isChecked())

    def restart(self):
        self.restartRequested.emit()

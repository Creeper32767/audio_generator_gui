from PySide6.QtCore import QMetaObject
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from qfluentwidgets import TextEdit, FluentIcon, SettingCardGroup, HyperlinkCard

from library import International


class InfoWindow(QMainWindow):
    def __init__(self, translator: International, version: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("LicenseWindow")

        # About
        self.developer_info_group = SettingCardGroup(translator.get_text('ui.about.developer.title'))
        self.view_on_github_card = HyperlinkCard(
            url="https://github.com/Creeper32767/audio_generator_gui",
            text=translator.get_text("ui.about.program.content"),
            icon=FluentIcon.GITHUB,
            title=translator.get_text('ui.about.program.content'),
            content=translator.get_text('ui.about.program.author').format(version),
            parent=self.developer_info_group
        )
        self.donation_card = HyperlinkCard(
            url="https://afdian.com/a/001c1f2ad",
            text=translator.get_text("ui.about.donation.content"),
            icon=FluentIcon.LINK,
            title=translator.get_text("ui.about.donation.title"),
            content=translator.get_text("ui.about.donation.content"),
            parent=self.developer_info_group
        )
        self.developer_info_group.addSettingCard(self.view_on_github_card)
        self.developer_info_group.addSettingCard(self.donation_card)

        # License text
        with open("LICENSE", encoding="utf-8") as fp:
            self.license_text = fp.read()

        # text editor to display license
        self.text_edit = TextEdit()
        self.text_edit.setPlainText(self.license_text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.developer_info_group)
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        QMetaObject.connectSlotsByName(self)

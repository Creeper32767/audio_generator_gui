from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import QMetaObject
from PySide6.QtGui import QFont, QFontDatabase
from qfluentwidgets import TextEdit, BodyLabel, FluentIcon, HeaderCardWidget, IconWidget, InfoBarIcon, \
    HyperlinkButton

from library import International


class DeveloperInfoCard(HeaderCardWidget):
    def __init__(self, dev_title: str, dev_content: str, version: str, view: str, custom_font, parent=None):
        super().__init__(parent)
        self.setTitle(dev_title)
        self.infoLabel = BodyLabel(dev_content.format(version), self)
        self.infoLabel.setFont(custom_font)

        self.infoIcon = IconWidget(InfoBarIcon.INFORMATION, self)
        self.hyperlink_button = HyperlinkButton(
            url="https://github.com/Creeper32767/audio_generator_gui",
            text=view,
            parent=self,
            icon=FluentIcon.GITHUB
        )

        self.vBoxLayout = QVBoxLayout()
        self.hBoxLayout = QHBoxLayout()

        self.infoIcon.setFixedSize(16, 16)
        self.hBoxLayout.setSpacing(10)
        self.vBoxLayout.setSpacing(16)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addWidget(self.infoIcon)
        self.hBoxLayout.addWidget(self.infoLabel)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.hyperlink_button)
        self.viewLayout.addLayout(self.vBoxLayout)


class InfoWindow(QMainWindow):
    def __init__(self, translator: International, version: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("LicenseWindow")
        # Load custom font
        font_id = QFontDatabase.addApplicationFont("assets/consola.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family)
        # Set font size
        custom_font.setPointSize(12)

        developer_info_card = DeveloperInfoCard(dev_title=translator.get_text('ui_about.developer.info'),
                                                dev_content=translator.get_text('ui_about.developer.content'),
                                                view=translator.get_text('ui_about.button_text'),
                                                version=version,
                                                custom_font=custom_font,
                                                parent=self)

        # License text
        with open("LICENSE", encoding="utf-8") as fp:
            self.license_text = fp.read()

        custom_font.setPointSize(10)
        # text editor to display license
        self.text_edit = TextEdit()
        self.text_edit.setPlainText(self.license_text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(custom_font)

        layout = QVBoxLayout()
        layout.addWidget(developer_info_card)
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        QMetaObject.connectSlotsByName(self)

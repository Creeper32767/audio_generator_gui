import json

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtCore import QThread, QTimer
from qfluentwidgets import TextEdit, PushButton, IndeterminateProgressBar, ComboBox, FluentIcon, Flyout, InfoBarIcon, \
    FlyoutAnimationType, GroupHeaderCardWidget, SpinBox, LineEdit, BodyLabel
from asyncio import run
from os.path import join, abspath

from library import TTSWorker, get_key_with_order, get_key_by_value_with_order, International


class GenerationWindow(QMainWindow):
    def __init__(self, translator: International, parent=None):
        """
        initialization the window for generating audio.

        Args:
            translator (International): tool to get text
            parent (_type_, optional): parent window. Defaults to None.
        """

        super().__init__(parent=parent)
        self.translator = translator
        self.path = None
        self.folder_path = None
        self.voice_short_name = list()
        self.setObjectName("GenerationWindow")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.vertical_layout = QVBoxLayout()
        central_widget.setLayout(self.vertical_layout)

        # create the second thread to fetch voices list
        self.thread = QThread(self)
        self.tts_generator = TTSWorker(
            (self.translator.get_text("ui_generation.choose_locale"),
            self.translator.get_text("ui_generation.choose_gender"),
            self.translator.get_text("ui_generation.choose_voice"))
        )
        self.tts_generator.moveToThread(self.thread)
        self.voice_info = run(self.tts_generator.fetch_voices_list())

        self.settngs_card = GroupHeaderCardWidget(parent=self)
        self.settngs_card.setTitle(self.translator.get_text("ui_generation.choice_title"))
        # choose locale
        self.voice_filter1 = ComboBox()
        self.voice_filter1.setMaxVisibleItems(10)
        self.voice_filter1.addItems(sorted(list(set(get_key_with_order(self.voice_info, 0, "")))))
        self.voice_filter1.currentTextChanged.connect(self.selection_changed)
        # choose gender
        self.voice_filter2 = ComboBox()
        self.voice_filter2.addItems(sorted(list(set(get_key_with_order(self.voice_info, 1, "")))))
        self.voice_filter2.currentTextChanged.connect(self.selection_changed)
        # all voices
        self.voice_filter3 = ComboBox()
        self.voice_filter3.setMaxVisibleItems(10)
        self.voice_filter3.addItems([self.translator.get_text("ui_generation.choose_voice")])
        # voice rate
        self.voice_rate_setter = SpinBox()
        self.voice_rate_setter.setRange(-99, 500)
        self.voice_rate_setter.setValue(0)
        # voice volume
        self.voice_volume_setter = SpinBox()
        self.voice_volume_setter.setRange(-99, 500)
        self.voice_volume_setter.setValue(0)
        # output path
        self.file_path_selector_widget = QWidget(parent=self)
        self.horizontal_layout = QHBoxLayout()
        self.file_path_selector_widget.setLayout(self.horizontal_layout)
        # button for opening folder browser
        self.file_path_selector = PushButton(self.translator.get_text("ui_generation.choose_folder_title").format(self.path), self)
        self.file_path_selector.clicked.connect(self.open_folder_dialog)
        self.horizontal_layout.addWidget(self.file_path_selector)
        # button for entering file name
        self.file_name_input = LineEdit()
        self.file_name_input.setText("output")
        self.file_name_input.textEdited.connect(self.update_path)
        self.horizontal_layout.addWidget(self.file_name_input)

        # join in layout
        self.settngs_card.addGroup("./assets/location.svg",
                                   self.translator.get_text("ui_generation.choose_locale_title"),
                                   self.translator.get_text("ui_generation.choose_locale_content"),
                                   self.voice_filter1)
        self.settngs_card.addGroup("./assets/music_note_1.svg",
                                   self.translator.get_text("ui_generation.choose_gender_title"),
                                   self.translator.get_text("ui_generation.choose_gender_content"),
                                   self.voice_filter2)
        self.settngs_card.addGroup("./assets/person_circle.svg",
                                   self.translator.get_text("ui_generation.choose_voice_title"),
                                   self.translator.get_text("ui_generation.choose_voice_content"),
                                   self.voice_filter3)
        self.settngs_card.addGroup("./assets/speed.svg",
                                   self.translator.get_text("ui_generation.enter_rate_title"),
                                   self.translator.get_text("ui_generation.enter_rate_content"),
                                   self.voice_rate_setter)
        self.settngs_card.addGroup("./assets/speaker_edit.svg",
                                   self.translator.get_text("ui_generation.enter_volume_title"),
                                   self.translator.get_text("ui_generation.enter_volume_content"),
                                   self.voice_volume_setter)
        self.settngs_card.addGroup(FluentIcon.FOLDER,
                                   self.translator.get_text("ui_generation.choose_folder_title"),
                                   self.translator.get_text("ui_generation.choose_folder_content"),
                                   self.file_path_selector_widget)
        self.vertical_layout.addWidget(self.settngs_card)

        # give information
        self.folder_label = BodyLabel(self.translator.get_text("ui_generation.show_path").format(""))
        self.vertical_layout.addWidget(self.folder_label)

        # area for entering text
        self.text_input = TextEdit()
        self.text_input.setPlaceholderText(self.translator.get_text("ui_generation.placeholder"))
        self.vertical_layout.addWidget(self.text_input)

        self.generate_button = PushButton(FluentIcon.PLAY, self.translator.get_text("ui_generation.generate"), self)
        self.generate_button.clicked.connect(self.generate_audio)
        self.vertical_layout.addWidget(self.generate_button)
        self.progress_bar = IndeterminateProgressBar()

    def selection_changed(self):
        selected_option1 = self.voice_filter1.currentText()
        selected_option2 = self.voice_filter2.currentText()

        # filter step 1 - locale
        if self.voice_filter1.currentIndex() != 0:
            self.voice_short_name = get_key_by_value_with_order(self.voice_info, selected_option1, 0)

        # filter step 2 - gender
        if self.voice_filter2.currentIndex() != 0:
            self.voice_short_name = list(filter(lambda x: self.voice_info[x][1] == selected_option2, self.voice_short_name))

        if not self.voice_short_name:
            self.voice_short_name = [self.translator.get_text("ui_generation.choose_voice")]
        self.voice_short_name.sort()

        # setting items
        self.voice_filter3.clear()
        self.voice_filter3.addItems(self.voice_short_name)
        self.voice_short_name.clear()

    def open_folder_dialog(self):
        # Open the folder browser dialog
        self.folder_path = QFileDialog.getExistingDirectory(self,
                                                            self.translator.get_text("ui_generation.choose_folder_title"),
                                                            "C:/")
        self.update_path()

    def update_path(self):
        # Update the label with the selected folder path
        if self.folder_path and self.file_name_input.text():
            self.path = abspath(join(self.folder_path, f"{self.file_name_input.text()}.mp3"))
            self.folder_label.setText(self.translator.get_text("ui_generation.show_path").format(self.path))
        else:
            self.folder_label.setText(self.translator.get_text("ui_generation.show_path").format("None"))

    def generate_audio(self):
        text = self.text_input.toPlainText()
        voice = self.voice_filter3.currentText()

        try:
            self.generate_button.setEnabled(False)
            # set values
            self.tts_generator.text = text
            self.tts_generator.voice = voice
            self.tts_generator.output_path = self.path
            self.tts_generator.rate = self.voice_rate_setter.value()
            self.tts_generator.volume = self.voice_volume_setter.value()
            # set hook
            self.thread.started.connect(self.tts_generator.run)
            self.thread.finished.connect(self.finishing)
            self.thread.start()
            self.vertical_layout.addWidget(self.progress_bar)
            self.thread.quit()

        except Exception as e:
            Flyout.create(
                icon=InfoBarIcon.ERROR,
                title='ERROR',
                content=self.translator.get_text("ui_generation.message.failed").format(e),
                target=self.generate_button,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.PULL_UP
            )
            self.progress_bar.deleteLater()
            self.generate_button.setEnabled(True)

    def finishing(self):
        # send messages
        flyout = Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='SUCCESS',
            content=self.translator.get_text("ui_generation.message.success"),
            target=self.generate_button,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
            )
        # automatically close the flyout after 1 second
        QTimer.singleShot(2000, flyout.close)
        self.progress_bar.deleteLater()
        self.progress_bar = IndeterminateProgressBar()
        self.generate_button.setEnabled(True)

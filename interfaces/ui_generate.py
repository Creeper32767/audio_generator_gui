from os.path import join, abspath
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtCore import QTimer, QThread
from qfluentwidgets import TextEdit, PushButton, IndeterminateProgressBar, ComboBox, FluentIcon, Flyout, InfoBarIcon, \
    FlyoutAnimationType, GroupHeaderCardWidget, SpinBox, LineEdit, BodyLabel

from library import get_key_with_order, get_key_by_value_with_order, International, BaseJsonOperator, TTSWorker


class GenerationWindow(QMainWindow):
    def __init__(self,
                 translator: International,
                 config: BaseJsonOperator,
                 theme: str,
                 tts_generator: TTSWorker,
                 parent=None):
        super().__init__(parent=parent)
        self.translator = translator
        self.config = config
        self.theme = theme

        # other variables
        self.path = None
        self.voice_short_name = list()
        self.setObjectName("GenerationWindow")

        self.tts_generator = tts_generator
        self.voice_info = self.tts_generator.indexes_with_head
        self.thread = QThread(self)
        self.tts_generator.moveToThread(self.thread)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.vertical_layout = QVBoxLayout()
        central_widget.setLayout(self.vertical_layout)

        self.settngs_card = GroupHeaderCardWidget(parent=self)
        self.settngs_card.setTitle(self.translator.get_text("ui_generation.choice_title"))
        # choose locale
        self.voice_filter1 = ComboBox()
        self.voice_filter1.setMaxVisibleItems(10)
        locale_list = sorted(list(set(get_key_with_order(self.voice_info, 0, ""))))
        self.voice_filter1.addItems(locale_list)
        self.voice_filter1.setText(locale_list[config.search("generate.location", 0)])
        self.voice_filter1.currentTextChanged.connect(self.filter_changed)
        self.voice_filter1.currentTextChanged.connect(self.selection_changed)
        # choose gender
        self.voice_filter2 = ComboBox()
        gender_list = sorted(list(set(get_key_with_order(self.voice_info, 1, ""))))
        self.voice_filter2.addItems(gender_list)
        self.voice_filter2.setText(gender_list[config.search("generate.gender", 0)])
        self.voice_filter2.currentTextChanged.connect(self.filter_changed)
        self.voice_filter2.currentTextChanged.connect(self.selection_changed)
        # all voices
        self.voice_filter3 = ComboBox()
        self.voice_filter3.setMaxVisibleItems(10)
        # voice rate
        self.voice_rate_setter = SpinBox()
        self.voice_rate_setter.setRange(-99, 500)
        self.voice_rate_setter.setValue(config.search("generate.speed", 0))
        self.voice_rate_setter.editingFinished.connect(self.selection_changed)
        # voice volume
        self.voice_volume_setter = SpinBox()
        self.voice_volume_setter.setRange(-99, 500)
        self.voice_volume_setter.setValue(config.search("generate.volume", 0))
        self.voice_volume_setter.editingFinished.connect(self.selection_changed)
        # output path
        self.file_path_selector_widget = QWidget(parent=self)
        self.horizontal_layout = QHBoxLayout()
        self.file_path_selector_widget.setLayout(self.horizontal_layout)
        # button for opening folder browser
        self.file_path_selector = PushButton(self.translator.get_text("ui_generation.choose_folder_title").format(self.path), self)
        self.file_path_selector.clicked.connect(self.open_folder_dialog)
        self.folder_path = self.config.search("generate.path", None)
        self.horizontal_layout.addWidget(self.file_path_selector)
        # button for entering file name
        self.file_name_input = LineEdit()
        self.file_name_input.setText(self.config.search("generate.audio_name", "output"))
        self.file_name_input.textEdited.connect(self.update_path)
        self.file_name_input.editingFinished.connect(self.selection_changed)
        self.horizontal_layout.addWidget(self.file_name_input)

        # join in layout
        self.settngs_card.addGroup(f"./assets/{self.theme}/location.svg",
                                   self.translator.get_text("ui_generation.choose_locale_title"),
                                   self.translator.get_text("ui_generation.choose_locale_content"),
                                   self.voice_filter1)
        self.settngs_card.addGroup(f"./assets/{self.theme}/music_note.svg",
                                   self.translator.get_text("ui_generation.choose_gender_title"),
                                   self.translator.get_text("ui_generation.choose_gender_content"),
                                   self.voice_filter2)
        self.settngs_card.addGroup(f"./assets/{self.theme}/person_circle.svg",
                                   self.translator.get_text("ui_generation.choose_voice_title"),
                                   self.translator.get_text("ui_generation.choose_voice_content"),
                                   self.voice_filter3)
        self.settngs_card.addGroup(f"./assets/{self.theme}/speed.svg",
                                   self.translator.get_text("ui_generation.enter_rate_title"),
                                   self.translator.get_text("ui_generation.enter_rate_content"),
                                   self.voice_rate_setter)
        self.settngs_card.addGroup(f"./assets/{self.theme}/speaker_edit.svg",
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
        self.filter_changed()
        self.progress_bar = IndeterminateProgressBar()

    def selection_changed(self):
        self.config.edit("generate.location", self.voice_filter1.currentIndex())
        self.config.edit("generate.gender", self.voice_filter2.currentIndex())
        self.config.edit("generate.speed", self.voice_rate_setter.value())
        self.config.edit("generate.volume", self.voice_volume_setter.value())
        self.config.edit("generate.path", self.folder_path)
        self.config.edit("generate.audio_name", self.file_name_input.text())

    def filter_changed(self):
        selected_option1 = self.voice_filter1.currentText()
        selected_index1 = self.voice_filter1.currentIndex()
        selected_option2 = self.voice_filter2.currentText()
        selected_index2 = self.voice_filter2.currentIndex()

        filtered_names = [self.translator.get_text("ui_generation.choose_voice")]

        # filter step 1 - locale
        if selected_index1 != 0:
            filtered_names = get_key_by_value_with_order(self.voice_info, selected_option1, 0)

        # filter step 2 - gender
        if selected_index2 != 0:
            filtered_names = [x for x in filtered_names if self.voice_info[x][1] == selected_option2]

        filtered_names.sort(key=lambda x: x.lower())
        self.voice_short_name = filtered_names

        # setting items
        self.voice_filter3.clear()
        self.voice_filter3.addItems(self.voice_short_name)

    def open_folder_dialog(self):
        # Open the folder browser dialog
        self.folder_path = QFileDialog.getExistingDirectory(self,
                                                            self.translator.get_text("ui_generation.choose_folder_title"),
                                                            "C:/")
        self.selection_changed()
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

        self.generate_button.setEnabled(False)
        # set values
        self.tts_generator.text = text
        self.tts_generator.voice = voice
        self.tts_generator.output_path = self.path
        self.tts_generator.rate = self.voice_rate_setter.value()
        self.tts_generator.volume = self.voice_volume_setter.value()
        # start thread
        self.thread.started.connect(self.tts_generator.starting_generating)
        self.tts_generator.finished.connect(self.finishing)
        self.tts_generator.finished.connect(self.thread.quit)
        self.tts_generator.error.connect(self.show_error_message)
        self.thread.start()
        self.vertical_layout.addWidget(self.progress_bar)

    def show_error_message(self, message: str):
        Flyout.create(
            icon=InfoBarIcon.ERROR,
            title='ERROR',
            content=self.translator.get_text("ui_generation.message.failed").format(message),
            target=self.generate_button,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
        )
        self.progress_bar.deleteLater()
        self.progress_bar = IndeterminateProgressBar()
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

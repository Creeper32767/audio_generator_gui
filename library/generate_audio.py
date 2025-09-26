import asyncio
from edge_tts import VoicesManager, Communicate
from PySide6.QtCore import Signal, QObject


class TTSWorker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self, voice_choice_message: tuple):
        super().__init__()
        self.voice_choice_message = voice_choice_message
        self.volume = None
        self.rate = None
        self.output_path = None
        self.voice = None
        self.text = None
        self.indexes_with_head = dict()
        self.indexes_common = dict()

    async def fetch_voice_list(self) -> tuple:
        voices = await VoicesManager.create()
        voices = voices.find()
        res_with_head = dict()
        res_common = dict()
        res_with_head[self.voice_choice_message[2]] = [self.voice_choice_message[0], self.voice_choice_message[1]]
        for voice in voices:
            res_with_head[voice["ShortName"]] = [voice["Locale"], voice["Gender"]]
            res_common[voice["ShortName"]] = [voice["Locale"], voice["Gender"]]

        return res_with_head, res_common

    async def generate_audio(self):
        """
        method for generating audio
        """        
        if self.rate >= 0:
            self.rate = f"+{self.rate}"
        if self.volume >= 0:
            self.volume = f"+{self.volume}"

        tts = Communicate(self.text, self.voice, rate=f"{self.rate}%", volume=f"{self.volume}%")
        tts.save_sync(self.output_path)

    def starting_fetching(self):
        try:
            indexes_with_head, indexes_common = asyncio.run(self.fetch_voice_list())
            self.indexes_with_head = indexes_with_head
            self.indexes_common = indexes_common
            self.finished.emit()
        except Exception as err:
            self.error.emit(str(err))

    def starting_generating(self):
        try:
            asyncio.run(self.generate_audio())
            self.finished.emit()
        except Exception as err:
            self.error.emit(str(err))

    def edit_voice_list(self, indexes_common: dict):
        self.indexes_common = indexes_common
        indexes_with_head = dict()
        indexes_with_head[self.voice_choice_message[2]] = [self.voice_choice_message[0], self.voice_choice_message[1]]
        for key, value in indexes_common.items():
            indexes_with_head[key] = value
        self.indexes_with_head = indexes_with_head

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
        self.voice_indexes = dict()

    async def fetch_voices_list(self):
        voices = await VoicesManager.create()
        voices = voices.find()
        res = dict()
        res[self.voice_choice_message[2]] = [self.voice_choice_message[0], self.voice_choice_message[1]]
        for voice in voices:
            res[voice["ShortName"]] = [voice["Locale"], voice["Gender"]]

        return res


    async def generate_audio(self, text: str, voice: str, output_path: str, rate: int, volume: int):
        """
        method for generating audio

        Args:
            text (str): the text that you need to transform
            voice (str): voice type
            output_path (str): where to write the audio file
            rate (int, optional): the additional speed of the audio
            volume (int, optional): the additional volume of the audio
        """        
        if rate >= 0:
            rate = f"+{rate}"
        if volume >= 0:
            volume = f"+{volume}"

        tts = Communicate(text, voice, rate=f"{rate}%", volume=f"{volume}%")
        tts.save_sync(output_path)

    def starting_fetching(self):
        try:
            indexes = asyncio.run(self.fetch_voices_list())
            self.voice_indexes = indexes
            self.finished.emit()
        except Exception as err:
            self.error.emit(str(err))

    def starting_generating(self):
        try:
            asyncio.run(self.generate_audio(self.text, self.voice, self.output_path, self.rate, self.volume))
            self.finished.emit()
        except Exception as err:
            self.error.emit(str(err))

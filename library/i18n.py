from library import json_ops
from os import listdir
from os.path import abspath, join
from typing import Any


class International(object):
    def __init__(self, locale: str, lang_path: str):
        """
        initialization.

        Args:
            locale (str): the region required for setting languages
        """

        self.locale = locale
        self.lang_path = abspath(lang_path)
        self.language_content = json_ops.read_json(join(self.lang_path, f"{self.locale}.json"))

        self.set_locale(self.locale)

    def set_locale(self, new_locale: str):
        """
        update current locale.

        Args:
            new_locale (str): the region required for setting languages
        """

        if new_locale in self.get_supported_languages():
            self.locale = new_locale
        else:
            self.locale = "en"
        self.language_content = json_ops.read_json(join(self.lang_path, f"{self.locale}.json"))

    def get_supported_languages(self) -> list:
        """
        update current locale.

        Returns:
            list: a list including all the supported languages
        """

        li_lang = listdir(self.lang_path)
        li_support_lang = list()
        for file in li_lang:
            if file.endswith(".json"):
                li_support_lang.append(file.split(".")[0])
            else:
                pass

        return li_support_lang


    def get_text(self, key: str) -> str:
        """
        get the correct text according to the value of locale.

        Args:
            key (str): the key you want for getting its text

        Returns:
            str: the text that follows the key
        """

        return json_ops.search(self.language_content, key)

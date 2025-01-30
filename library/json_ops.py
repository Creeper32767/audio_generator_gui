import json
from os import listdir
from os.path import abspath, join
from typing import Union, Any


class BaseJsonOperator(object):
    def __init__(self, file_path: str):
        """
        Initialize an object from a json file.

        Args:
            file_path (str): the file path (relative and absolute path are both supported.)
        """
        self.file_path = abspath(file_path)
        try:
            with open(file_path, encoding="utf-8") as fp:
                self.json_content = json.load(fp)
        except FileNotFoundError:
                with open(file_path, encoding="utf-8", mode="w"):
                    self.json_content = dict()

    def write_json(self) -> None:
        """
        Write content to a json file.
        """

        with open(self.file_path, encoding="utf-8", mode="w") as fp:
            json.dump(self.json_content, fp, indent=2)

    def search(self, key: str, default_value: Union[str, Any] = "Error") -> Union[str, Any]:
        """
        Read content from a dictionary.

        Args:
            key (str): the key in the dictionary
            default_value (Any): the content to return when the key isn't found

        Returns:
            Union[str, Any]: the value that follows the key
        """

        try:
            return self.json_content[key]
        except KeyError:
            if default_value != "Error":
                self.edit(key, default_value)
            return default_value

    def edit(self, key: str, new_value: Any):
        """
        Edit content in a dictionary. It will add a key to the dictionary if the key doesn't exist.

        Args:
            key (str): the key in the dictionary
            new_value (Any): the value that you want to use for replacement

        Returns:
            Union[str, None]: the possible return message
        """

        self.json_content[key] = new_value
        self.write_json()


class International(BaseJsonOperator):
    def __init__(self, locale: str, lang_path: str):
        """
        Initialization.

        Args:
            locale (str): the region required for setting languages
            lang_path (str): the relative path of the folder that stores the language files
        """

        super().__init__(join(lang_path, f"{locale}.json"))
        self.locale = locale
        self.lang_path = lang_path

        self.supported_languages = self.get_supported_languages()

    def set_locale(self, new_locale: str) -> None:
        """
        Update current locale.

        Args:
            new_locale (str): the region required for setting languages
        """

        if new_locale in self.supported_languages:
            self.locale = new_locale
        else:
            self.locale = "en"

        self.__init__(self.locale, self.lang_path)

    def get_supported_languages(self) -> list:
        """
        Get supported languages.

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
        Get the correct text according to the value of locale.

        Args:
            key (str): the key you want for getting its text

        Returns:
            str: the text that follows the key
        """

        return self.search(key)

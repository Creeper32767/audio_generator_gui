import json
from os import listdir
from os.path import abspath, join
from typing import Union, Any


class BaseJsonOperator(object):
    def __init__(self, file_path: str):
        """
        Initialize an object from a json file.

        :param file_path: The file path (relative and absolute path are both supported).
        """
        self.file_path = abspath(file_path)
        try:
            with open(file_path, encoding="utf-8") as fp:
                self.json_content = json.load(fp)
        except FileNotFoundError:
                with open(file_path, encoding="utf-8", mode="w") as fp:
                    self.json_content = dict()
                    fp.write("{\n}")

    def write_json(self) -> None:
        """
        Write content to a json file.
        """
        with open(self.file_path, encoding="utf-8", mode="w") as fp:
            json.dump(self.json_content, fp, indent=2, sort_keys=True)

    def search(self,
               key: str,
               default_value: Union[str, Any] = "Error",
               verification_types: Union[set, tuple, list, None] = None,
               verification_not_types: Union[set, tuple, list, None] = None,
               verification_in: Union[set, tuple, list, None] = None,
               verification_not_in: Union[set, tuple, list, None] = None
    ) -> Any:
        """
        Read value from a dictionary and return it.

        :param key: Key you required in the dictionary.
        :param default_value: Content to return when the key isn't found.
        :param verification_types: Types the value should be.
        :param verification_not_types: Types the value shouldn't be.
        :param verification_in: Values the value should be one of them.
        :param verification_not_in: Values the value shouldn't be one of them.

        :return: The value that follows the key.
        """
        try:
            res = self.json_content[key]
            # Verification
            if verification_types is not None:
                if type(res) not in verification_types:
                    self.save_default_value(key, default_value)
                    return default_value
            if verification_not_types is not None:
                if type(res) in verification_not_types:
                    self.save_default_value(key, default_value)
                    return default_value
            if verification_in is not None:
                if res not in verification_in:
                    self.save_default_value(key, default_value)
                    return default_value
            if verification_not_in is not None:
                if res in verification_not_in:
                    self.save_default_value(key, default_value)
                    return default_value

            return res
        except KeyError:
            self.save_default_value(key, default_value)
            return default_value

    def save_default_value(self, key: Any, default_value: Any):
        # Sync values to the file
        if default_value != "Error":
            self.edit(key, default_value)
        else:
            self.edit(key, "")

    def edit(self, key: str, new_value: Any):
        """
        Edit content in a dictionary. It will add a key to the dictionary if the key doesn't exist.

        :param key: Key you required in the dictionary.
        :param new_value: The value that you want to use for replacement.
        """
        self.json_content[key] = new_value
        self.write_json()


class International(BaseJsonOperator):
    def __init__(self, locale: str, lang_path: str):
        """
        Initialization.

        :param locale: Region(language name like 'zh-cn') required for setting languages.
        :param lang_path: Relative path of the folder that stores the language files.
        """
        super().__init__(join(lang_path, f"{locale}.json"))
        self.locale = locale
        self.lang_path = lang_path

        self.supported_languages = self.get_supported_languages()

    def set_locale(self, new_locale: str) -> None:
        """
        Update current locale.

        :param new_locale: Region required for setting languages.
        """
        if new_locale in self.supported_languages:
            self.locale = new_locale
        else:
            self.locale = "en"

        self.__init__(self.locale, self.lang_path)

    def get_supported_languages(self) -> list:
        """
        Get supported languages.

        :return: A list including all the supported languages.
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

        :param key: Key you required for getting its text.

        :return: Translated text that follows the key.
        """
        return self.search(key, verification_types=[list, str])

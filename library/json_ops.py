import json
from os.path import abspath
from typing import Union, Any


def read_json(file_path: str) -> dict:
    """
    read content from a json file.

    Args:
        file_path (str): the file path

    Returns:
        dict: file content
    """

    with open(abspath(file_path), encoding="utf-8") as fp:
        try:
            return json.load(fp)
        except FileNotFoundError:
            with open(abspath(file_path), encoding="utf-8", mode="w") as fp:
                fp.write("""{
  "locale": "en",
  "theme": "AUTO"
}""")
            read_json(file_path)


def write_json(content: dict, file_path: str) -> None:
    """
    write content to a json file.

    Args:
        content (dict): the content you'd like to save
        file_path (str): the file path
    """

    with open(abspath(file_path), encoding="utf-8", mode="w") as fp:
        json.dump(content, fp, indent=2)


def search(dictionary: dict, key: str) -> Union[str, Any]:
    """
    read content from a dictionary.

    Args:
        dictionary (dict): the data source
        key (str): the key in the dictionary

    Returns:
        Union[str, Any]: the value that follows the key
    """

    try:
        return dictionary[key]
    except KeyError:
        return "Error"


def edit(file_path: str, key: str, new_value: Any) -> Union[str, None]:
    """
    edit content in a dictionary.

    Args:
        file_path (dict): the data source
        key (str): the key in the dictionary
        new_value (Any): the value that you want to use for replacement

    Returns:
        Union[str, None]: the possible return message
    """
    dictionary = read_json(file_path)

    if key in dictionary.keys():
        dictionary[key] = new_value
        write_json(dictionary, file_path)
    else:
        return "Error"

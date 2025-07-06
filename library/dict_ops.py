from typing import Any


def get_key_with_order(dictionary: dict, order: int, completion: Any = "") -> list:
    """
    Get the key with certain order, use it when the keys of a dictionary are lists.

    :param dictionary: The dictionary
    :param order: The order that you want to get elements at
    :param completion: The thing to add when there is no element at the order

    :return: Elements at the order
    """
    return [value[order] if order < len(value) else completion for value in dictionary.values()]


def get_key_by_value(dictionary: dict, target_value: Any) -> list:
    """
    Get the key in a dictionary according to the value.

    :param dictionary: The dictionary
    :param target_value: The value you'd like to search

    :return: Keys that match the target_value
    """
    return [key for key, value in dictionary.items() if value == target_value]


def get_key_by_value_with_order(dictionary: dict, target_value: Any, order: int) -> list:
    """
    Get the key in a dictionary according to the value, meanwhile, the value is at certain order of a list.

    :param dictionary: The dictionary
    :param target_value: The value you'd like to search
    :param order: The order that the element you want is at

    :return: Keys that match the target_value
    """
    return [key for key, value in dictionary.items() if order < len(value) and value[order] == target_value]

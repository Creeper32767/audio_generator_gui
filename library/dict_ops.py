from typing import Any


def get_key_with_order(dictionary: dict, order: int, completion: Any = "") -> list:
    """
    get the key with certain order, use it when the keys of a dictionary are lists

    Args:
        dictionary (dict): the dictionary
        order (int): the order that you want to get elements at this order
        completion (Any): the thing to add when there is no element at the order

    Returns:
        list: the elements at the order
    """

    res = list()
    try:
        for value in dictionary.values():
            res.append(value[order])
    except IndexError:
        res.append(completion)

    return res


def get_key_by_value(dictionary: dict, target_value: Any) -> list:
    """
    get the key in a dictionary according to the value.

    Args:
        dictionary (dict): the dictionary
        target_value (Any): the value you'd like to search

    Returns:
        list: the keys that match the target_value
    """

    res = list()
    for key, value in dictionary.items():
        if value == target_value:
            res.append(key)

    return res


def get_key_by_value_with_order(dictionary: dict, target_value: Any, order: int) -> list:
    """
    get the key in a dictionary according to the value, meanwhile, the value is at certain order

    Args:
        dictionary (dict): the dictionary
        target_value (Any): the value you'd like to search
        order (int): the order that the element you want is at

    Returns:
        list: the keys that match the target_value
    """

    res = list()
    for key, value in dictionary.items():
        if value[order] == target_value:
            res.append(key)

    return res

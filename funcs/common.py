import json


def read_json(file_json: str) -> dict:
    """Read JSON file to dictionary

    :param file_json:
    :return:
    """
    with open(file_json) as f:
        dict_init = json.load(f)
        return dict_init

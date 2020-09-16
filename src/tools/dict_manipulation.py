from typing import Dict


def flat_dict(dictionary: Dict) -> Dict:
    ret = dict(dictionary)
    for key, values in dictionary.items():
        flat_list = []
        for value in values:
            if isinstance(value, list):
                flat_list.extend(value)
            else:
                flat_list.append(value)
        ret[key] = flat_list
    return ret
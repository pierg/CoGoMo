import hashlib
import random
import string


def get_name_and_id(value: str = None):
    if value is None:
        name: str = ""

        """5 character ID generated from a random string"""
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        id = hashlib.sha1(random_string.encode("UTF-8")).hexdigest()[:5]
    else:
        name: str = value

        """5 character ID generated from the name"""
        id: str = hashlib.sha1(value.encode("UTF-8")).hexdigest()[:5]

    return name, id

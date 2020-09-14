

class Name(object):
    """A data descriptor for name
    """

    def __init__(self, value):
        self._name = value

    def __get__(self, owner_instance, owner_type):
        return self._name

    def __set__(self, owner_instance, value):
        self._name = value


def set_name(self, name):
    print('setname() called')
    self.__name = name


def get_name(self):
    print('getname() called')
    return self.__name


def del_name(self):
    print('delname() called')
    del self.__name
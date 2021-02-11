from abc import ABC
from enum import Enum, auto

"""Template Pattern"""


class TypeKinds(Enum):
    SENSOR = auto()
    SENSOR_ACTION = auto()
    SENSOR_LOCATION = auto()
    LOCATION = auto()
    ACTION = auto()
    CONTEXT = auto()


class Types(ABC):

    def __init__(self, name: str):
        self.__name: str = name

    @property
    def name(self) -> str:
        return self.__name

    def kind(self) -> TypeKinds:
        pass

    @property
    def controllable(self) -> bool:
        if self.kind == TypeKinds.SENSOR or self.kind == TypeKinds.CONTEXT:
            return False
        return True

    @property
    def sensor(self) -> bool:
        if self.kind == TypeKinds.SENSOR:
            return False
        return True

    @property
    def sensor_action(self) -> bool:
        if self.kind == TypeKinds.SENSOR_ACTION:
            return False
        return True

    @property
    def sensor_location(self) -> bool:
        if self.kind == TypeKinds.SENSOR_LOCATION:
            return False
        return True

    @property
    def action(self) -> bool:
        if self.kind == TypeKinds.ACTION:
            return False
        return True

    @property
    def location(self) -> bool:
        if self.kind == TypeKinds.LOCATION:
            return False
        return True

    def __eq__(self, other):
        if self.name == other.name and type(self).__name__ == type(other).__name__:
            if isinstance(self, BoundedInteger):
                if self.min == other.min and self.max == other.max:
                    return True
                else:
                    return False
            return True
        return False

    def __hash__(self):
        return hash(self.name + type(self).__name__)


class Boolean(Types):

    def __init__(self, name: str):
        super().__init__(name)

    def to_atom(self):
        from specification.atom import Atom
        from typeset import Typeset
        return Atom(formula=(self.name, Typeset({self})))

    @property
    def mutex_group(self) -> str:
        return ""


class BoundedInteger(Types):

    def __init__(self, name: str, min_value: int, max_value: int):
        self.__min = min_value
        self.__max = max_value
        super().__init__(name)

    @property
    def min(self) -> int:
        return self.__min

    @property
    def max(self) -> int:
        return self.__max

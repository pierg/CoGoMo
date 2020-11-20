from type import BoundedInteger, Boolean, TypeKinds


class IntegerAction(BoundedInteger):

    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)

    @property
    def kind(self):
        return TypeKinds.ACTION


class BooleanAction(Boolean):

    def __init__(self, name: str):
        super().__init__(name)

    @property
    def kind(self):
        return TypeKinds.ACTION

from goal.cgg import Node, Link


class Orchestrator:

    def __init__(self,
                 cgg: Node):
        self.cgg = cgg

    @property
    def cgg(self) -> Node:
        return self.__cgg

    @cgg.setter
    def cgg(self, value: Node):
        self.__cgg = value
        self.contextual_controllers = []

        for goal in self.cgg.children[Link.DISJUNCTION]:
            self.contextual_controllers.append((goal.context, goal.controller))

    # def orchestrate(self, steps: int):
    #
    #     for i in range(steps):

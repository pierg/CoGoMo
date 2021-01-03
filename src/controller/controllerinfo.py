from typing import List


class ControllerInfo:

    def __init__(self,
                 assumptions: List[str] = None,
                 a_liveness: List[str] = None,
                 a_mutex: List[str] = None,
                 guarantees: List[str] = None,
                 g_mutex: List[str] = None,
                 g_adjacency: List[str] = None,
                 inputs: List[str] = None,
                 outputs: List[str] = None):
        self.__assumptions = assumptions
        self.__a_liveness = a_liveness
        self.__a_mutex = a_mutex
        self.__guarantees = guarantees
        self.__g_mutex = g_mutex
        self.__g_adjacency = g_adjacency
        self.__inputs = inputs
        self.__outputs = outputs

    @property
    def assumptions(self):
        return self.__assumptions

    @property
    def a_liveness(self):
        return self.__a_liveness

    @property
    def a_mutex(self):
        return self.__a_mutex

    @property
    def guarantees(self):
        return self.__guarantees

    @property
    def g_mutex(self):
        return self.__g_mutex

    @property
    def g_adjacency(self):
        return self.__g_adjacency

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def save_to_file(path: str):
        pass

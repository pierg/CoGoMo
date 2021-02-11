import itertools
from typing import List, Tuple

from tools.logic import Logic


class ControllerInfo:

    def __init__(self,
                 a_initial: List[str] = None,
                 a_fairness: List[str] = None,
                 a_safety: List[str] = None,
                 a_mutex: List[str] = None,
                 g_initial: List[str] = None,
                 g_safety: List[str] = None,
                 g_mutex: List[str] = None,
                 g_goal: List[str] = None,
                 inputs: List[str] = None,
                 outputs: List[str] = None):
        self.__a_initial = a_initial
        self.__a_fairness = a_fairness
        self.__a_safety = a_safety
        self.__a_mutex = a_mutex
        self.__g_initial = g_initial
        self.__g_mutex = g_mutex
        self.__g_safety = g_safety
        self.__g_goal = g_goal
        self.__inputs = inputs
        self.__outputs = outputs

    @property
    def a_initial(self):
        return self.__a_initial

    @property
    def a_fairness(self):
        return self.__a_fairness

    @property
    def a_safety(self):
        return self.__a_safety

    @property
    def a_mutex(self):
        return self.__a_mutex

    @property
    def g_initial(self):
        return self.__g_initial

    @property
    def g_mutex(self):
        return self.__g_mutex

    @property
    def g_safety(self):
        return self.__g_safety

    @property
    def g_goal(self):
        return self.__g_goal

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def get_strix_inputs(self) -> Tuple[str, str, str, str]:
        a = Logic.and_(list(itertools.chain(
            self.__a_initial,
            self.__a_fairness,
            self.__a_safety,
            self.__a_mutex
        )))
        from tools.strings import StringMng
        a = StringMng.strix_syntax_fix(a)

        g = Logic.and_(list(itertools.chain(
            self.__g_initial,
            self.__g_mutex,
            self.__g_safety,
            self.__g_goal
        )))
        g = StringMng.strix_syntax_fix(g)

        i = " ,".join(self.__inputs)
        o = " ,".join(self.__outputs)

        return a, g, i, o

    def save_to_file(path: str):
        pass

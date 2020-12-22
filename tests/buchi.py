from specification.atom.pattern.dwyer.scopes import P_global
from tools.spot import Spot


def robotic_patterns():
    # Dwyer
    Spot.generate_buchi(P_global(p=LTL("p")), "P_global")


if __name__ == '__main__':
    robotic_patterns()
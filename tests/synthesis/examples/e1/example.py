import os

from tools.strings.logic import Implies
from controller.parser import parse_controller
from controller.synthesis import create_controller_if_exists
from tools.strings_manipulation import save_to_file

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"

a, g, i, o = parse_controller(folder_path + "specification.txt")
assumptions = a.replace("TRUE", "true")
guarantees = g.replace("TRUE", "true")
params = ' -k --dot -f "' + Implies(assumptions, guarantees) + '" --ins="' + i + '" --outs="' + o + '"'

save_to_file(params, folder_path + "specification_params.txt")
create_controller_if_exists(folder_path + "specification.txt")
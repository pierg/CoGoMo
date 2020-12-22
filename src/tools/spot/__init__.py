import subprocess
import os
from graphviz import Source
from tools.storage import Store

from specification import Specification

results_folder = os.path.dirname(os.path.abspath(__file__)) + "/output/"


class Spot:

    @staticmethod
    def generate_buchi(spec: Specification, name: str, save_to: str = None):
        if save_to is not None:
            results_folder = save_to
        try:
            dot_file_path = os.path.dirname(name)
            if dot_file_path == "":
                name = results_folder + name

            formula_str = spec.formula()[0]

            result = subprocess.check_output(["ltl2tgba", "-B", formula_str, "-d"], encoding='UTF-8',
                                             stderr=subprocess.DEVNULL).splitlines()
            result = [x for x in result if not ('[Büchi]' in x)]
            result = "".join(result)

            dot_file_path = os.path.dirname(name)
            dot_file_name = os.path.splitext(name)[0]

            Store.save_to_file(result, dot_file_name + ".dot")
            src = Source(result, directory=dot_file_path, filename=dot_file_name, format="eps")
            src.render(cleanup=True)
            print(dot_file_name + ".eps  ->   buchi generated")

        except Exception as e:
            raise e




import os
from pathlib import Path

from graphviz import Source


class Store:
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output'))

    @staticmethod
    def save_to_file(text: str, folder_name: str, file_name: str):

        if Path(file_name).suffix is None:
            file_name += ".txt"

        output_folder = f"{Store.output_folder}/{folder_name}"
        output_file = f"{output_folder}/{file_name}"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_file, 'w') as f:
            f.write(text)

        f.close()

    @staticmethod
    def generate_eps_from_dot(dot_mealy: str, folder_name: str, file_name: str):

        Store.save_to_file(dot_mealy, folder_name, f"{file_name}_dot.txt")

        output_folder = f"{Store.output_folder}/{folder_name}"

        source = Source(dot_mealy, directory=output_folder, filename=file_name, format="eps")
        source.render(cleanup=True)
        print(f"{output_folder}/{file_name} -> DOT and EPS files generated")

        return source


if __name__ == '__main__':
    Store.save_to_file("ciao", "folder/message/file.txt")

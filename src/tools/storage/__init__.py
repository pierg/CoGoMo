import os


class Store:
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output'))

    @staticmethod
    def save_to_file(text: str, file_path: str):

        dir_name, file_name = os.path.split(file_path)
        output_folder = Store.output_folder + "/" + dir_name
        output_file = output_folder + "/" + file_name

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_file, 'w') as f:
            f.write(text)

        f.close()


if __name__ == '__main__':
    Store.save_to_file("ciao", "folder/message/file.txt")
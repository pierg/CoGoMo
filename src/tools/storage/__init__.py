import os

class Store:

    @staticmethod
    def save_to_file(text: str, file_path: str):
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(file_path, 'w') as f:
            f.write(text)

        f.close()

import os

from controller.synthesis import synthesis_from_txt_spec

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"

synthesis_from_txt_spec(folder_path)
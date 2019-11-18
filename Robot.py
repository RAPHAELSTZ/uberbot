from Params import Params
import os, shutil


class Robot:

    def __init__(self, reports="normal"):
        self.config = Params()


    def expand_config(self, key):
        if key in self.config.robot:
            self.config.robot[key] = os.path.normpath(os.path.expanduser(self.config.robot[key]))

    def get_folder_path(self, key_dir):
        dir_path = key_dir
        if key_dir in self.config.robot:
            dir_path = self.config.robot[key_dir]
        
        return dir_path

    def get_file_path(self, key_dir, file_name_or_key):
        dir_path = self.get_folder_path(key_dir)

        file_name = file_name_or_key
        if file_name_or_key in self.config.robot:
            file_name = self.config.robot[file_name_or_key]

        return os.path.join(dir_path, file_name)

    def clear_dir(self, key_dir):
        dir_path = self.get_folder_path(key_dir)
        shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)


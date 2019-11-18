import json
import os
import sys
import getopt
import uuid
from subprocess import Popen
from sys import platform


# Singleton class
class Params:
    instance = None

    """
    Récupère la variable d'environnement correspondante au paramètre key
    """
    @staticmethod
    def get_env_var(key):
        environ = os.environ
        return environ.get(key)

    """
    Recherche les arguments passés en ligne de commande
    """
    @staticmethod
    def get_input_files(robot_code_name, exec_id):
        if platform == "win32":
            Popen(Params().robot["powershellScriptPath"] + robot_code_name + " " + exec_id)

    @staticmethod
    def get_args():
        argv = sys.argv[1:]
        result = {"init": "", "user": "robot", "pid": uuid.uuid4().hex, "env": "dev"}
        return result

    class __Params:
        def __init__(self, config_folder=None):

            self.robotParamsDict = dict()
            self.userParamsDict = dict()
            args = Params.get_args()
            platform = sys.platform

            print("Plateforme détectée : %s." % platform)
            print("Vérification des paramètres d'entrées: ")
            print("Script initial:\t\t\t %s" % sys.argv[0])
            if "init" in args:
                config_folder = args["init"]
                print("Dossier init:\t\t\t %s" % config_folder)
                print("Le dossier existe:\t\t %s" % os.path.isdir(config_folder))

            if config_folder is None or config_folder == "":
                folder_path = os.getcwd() + "/init"
                print("Utilisation du chemin actuel : %s." % folder_path)

            else:
                print("Utilisation du chemin en paramètre: %s." % config_folder)
                folder_path = config_folder

            robot_param_file = folder_path + '/robot_params.json'
            user_param_file = folder_path + '/user_params.json'

            if not os.path.isfile(robot_param_file):
                raise RuntimeError("Fichier de configuration du robot introuvable : %s" % robot_param_file)
            else:
                with open(robot_param_file, encoding='utf-8') as json_data:
                    self.robotParamsDict = json.load(json_data)
            if not os.path.isfile(user_param_file):
                print("Warning: Fichier de configuration utilisateur introuvable : %s" % user_param_file)
            else:
                with open(user_param_file, encoding='utf-8') as json_data:
                    self.userParamsDict = json.load(json_data)
            if len(args) > 0:
                self.robotParamsDict = {**self.robotParamsDict, **args}

    def __init__(self, config_folder=None):
        if not Params.instance:
            Params.instance = Params.__Params(config_folder)

    def __getattr__(self, name):
        if name == 'robot' or name == 'user':
            name = name + 'ParamsDict'
        return getattr(self.instance, name)

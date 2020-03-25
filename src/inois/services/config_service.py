import os
from inois.models.config import Config
from inois.utils.notifications import Notifications


class ConfigService:

    @classmethod
    def initialize_config(cls, input_file):
        input_settings = cls.read_input(input_file)
        cls.validate_input(input_settings)
        return cls.set_config(input_settings)

    @staticmethod
    def read_input(input_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError("Input file '{0}' was not found.".format(input_file))

        try:
            with open(input_file, encoding='utf-8') as file:
                config = eval(file.read())
                assert isinstance(config, dict)
                return config
        except SyntaxError:
            print(Notifications.INVALID_INPUT_FILE_ERROR.format(input_file))
            raise TypeError("Can't convert input file '{0}' to type 'dictionary'. File must be re-formatted to continue".format(input_file))

    @staticmethod
    def validate_input(input_dictionary):
        for key in input_dictionary:
            if key not in Config.KEYS:
                raise ValueError("Key type '{0}' is not supported".format(key))

        if Config.KEYS[0] in input_dictionary:
            if not isinstance(input_dictionary[Config.KEYS[0]], str):
                raise ValueError("Config key '{0}' must be a string, but '{1}' is a {2}".format(Config.KEYS[0], input_dictionary[Config.KEYS[0]], type(input_dictionary[Config.KEYS[0]])))

        if Config.KEYS[1] in input_dictionary:
            if not isinstance(input_dictionary[Config.KEYS[1]], list):
                raise ValueError("Config key '{0}' must be a list, but '{1}' is a {2}".format(Config.KEYS[1], input_dictionary[Config.KEYS[1]], type(input_dictionary[Config.KEYS[1]])))
            else:
                for file in input_dictionary[Config.KEYS[1]]:
                    if not isinstance(file, str):
                        raise ValueError("Values listed for config key '{0}' must be strings, but '{1}' is a {2}".format(Config.KEYS[1], file, type(file)))

        if Config.KEYS[2] in input_dictionary:
            if not isinstance(input_dictionary[Config.KEYS[2]], list):
                raise ValueError("Config key '{0}' must be a list, but '{1}' is a {2}".format(Config.KEYS[2], input_dictionary[Config.KEYS[2]], type(input_dictionary[Config.KEYS[2]])))
            else:
                for column in input_dictionary[Config.KEYS[2]]:
                    if not isinstance(column, str):
                        raise ValueError("Values listed for config key '{0}' must be strings, but '{1}' is a {2}".format(Config.KEYS[1], column, type(column)))

        if Config.KEYS[3] in input_dictionary:
            if not isinstance(input_dictionary[Config.KEYS[3]], str):
                raise ValueError("Config key '{0}' must be a string, but '{1}' is a {2}".format(Config.KEYS[3], input_dictionary[Config.KEYS[3]], type(input_dictionary[Config.KEYS[3]])))

    @staticmethod
    def set_config(input_dictionary):
        config = Config(input_dictionary)
        print(config)
        return config

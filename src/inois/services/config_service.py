import os
from inois.models.config import Config
from inois.utils.notifications import Notifications
from inois.utils.config_keys import ConfigKeys


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

    @classmethod
    def validate_input(cls, input_dictionary):
        for key in input_dictionary:
            if key not in ConfigKeys.VALID_KEYS:
                raise ValueError("Key type '{0}' is not supported".format(key))

        if ConfigKeys.WORKING_DIRECTORY in input_dictionary:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.WORKING_DIRECTORY)

        if ConfigKeys.FILES in input_dictionary:
            cls.validate_input_is_list_of_strings(input_dictionary, ConfigKeys.FILES)

        if ConfigKeys.COLUMNS_TO_HASH in input_dictionary:
            cls.validate_input_is_list_of_strings(input_dictionary, ConfigKeys.COLUMNS_TO_HASH)

        if ConfigKeys.USERNAME in input_dictionary:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.USERNAME)

    @staticmethod
    def set_config(input_dictionary):
        config = Config(input_dictionary)
        print(config)
        return config

    @staticmethod
    def validate_input_is_string(input_dictionary, key):
        if not isinstance(input_dictionary[key], str):
            raise ValueError("Config key '{0}' must be a string, but '{1}' is a {2}".format(key, input_dictionary[key], type(input_dictionary[key])))

    @staticmethod
    def validate_input_is_list_of_strings(input_dictionary, key):
        if not isinstance(input_dictionary[key], list):
            raise ValueError("Config key '{0}' must be a list, but '{1}' is a {2}".format(key, input_dictionary[key], type(input_dictionary[key])))
        else:
            for item in input_dictionary[key]:
                if not isinstance(item, str):
                    raise ValueError("Values listed for config key '{0}' must be strings, but '{1}' is a {2}".format(key, item, type(item)))

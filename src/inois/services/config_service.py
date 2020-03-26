import os
import logging
from inois.models.config import Config
from inois.utils.notifications import Notifications
from inois.utils.config_keys import ConfigKeys


class ConfigService:

    @classmethod
    def initialize_config(cls, input_file):
        logging.info("Initializing Config...")
        input_settings = cls.read_input(input_file)
        cls.validate_input(input_settings)
        return cls.set_config(input_settings)

    @staticmethod
    def read_input(input_file):
        logging.debug("reading input file - {0}".format(input_file))
        if not os.path.exists(input_file):
            logging.error(Notifications.FILE_NOT_FOUND_ERROR.format(input_file))
            raise FileNotFoundError(Notifications.FILE_NOT_FOUND_ERROR.format(input_file))

        try:
            with open(input_file, encoding='utf-8') as file:
                config = eval(file.read())
                assert isinstance(config, dict)
                return config
        except SyntaxError:
            logging.error(Notifications.INVALID_INPUT_FILE_ERROR.format(input_file))
            raise TypeError(Notifications.INVALID_INPUT_FILE_ERROR.format(input_file))

    @classmethod
    def validate_input(cls, input_dictionary):
        logging.debug("validating input file")
        for key in input_dictionary:
            if key not in ConfigKeys.VALID_KEYS:
                logging.error(Notifications.INVALID_KEY_ERROR.format(key))
                raise ValueError(Notifications.INVALID_KEY_ERROR.format(key))

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
        logging.debug("setting application config")
        config = Config(input_dictionary)
        logging.info(config)
        print(config)
        return config

    @staticmethod
    def validate_input_is_string(input_dictionary, key):
        if not isinstance(input_dictionary[key], str):
            logging.error(Notifications.INVALID_CONFIG_VALUE_TYPE_ERROR.format(key, "string", input_dictionary[key], type(input_dictionary[key])))
            raise ValueError(Notifications.INVALID_CONFIG_VALUE_TYPE_ERROR.format(key, "string", input_dictionary[key], type(input_dictionary[key])))

    @staticmethod
    def validate_input_is_list_of_strings(input_dictionary, key):
        if not isinstance(input_dictionary[key], list):
            logging.error(Notifications.INVALID_CONFIG_VALUE_TYPE_ERROR.format(key, "list", input_dictionary[key], type(input_dictionary[key])))
            raise ValueError(Notifications.INVALID_CONFIG_VALUE_TYPE_ERROR.format(key, "list", input_dictionary[key], type(input_dictionary[key])))
        else:
            for item in input_dictionary[key]:
                if not isinstance(item, str):
                    logging.error(Notifications.INVALID_LIST_ITEM_TYPE_ERROR.format(key, "strings", item, type(item)))
                    raise ValueError(Notifications.INVALID_LIST_ITEM_TYPE_ERROR.format(key, "strings", item, type(item)))

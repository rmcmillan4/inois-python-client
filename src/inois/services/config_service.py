import os
import logging
from datetime import datetime
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
        logging.debug("reading input file '{0}'".format(input_file))
        if not os.path.exists(input_file):
            logging.error(Notifications.FILE_NOT_FOUND_ERROR.format(input_file))
            raise FileNotFoundError(Notifications.FILE_NOT_FOUND_ERROR.format(input_file))

        try:
            with open(input_file, encoding='utf-8') as file:
                config = eval(file.read())
                assert isinstance(config, dict)
                return config
        except SyntaxError:
            logging.error(Notifications.INVALID_INPUT_FILE_FORMAT_ERROR.format(input_file))
            raise TypeError(Notifications.INVALID_INPUT_FILE_FORMAT_ERROR.format(input_file))

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

        if ConfigKeys.AUTHENTICATION_SCOPE not in input_dictionary:
            logging.error(Notifications.REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR.format(ConfigKeys.AUTHENTICATION_SCOPE))
            raise ValueError(Notifications.REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR.format(ConfigKeys.AUTHENTICATION_SCOPE))
        else:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.AUTHENTICATION_SCOPE)

        if ConfigKeys.AUTHENTICATION_TENANT_AUTHORITY not in input_dictionary:
            logging.error(Notifications.REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR.format(ConfigKeys.AUTHENTICATION_TENANT_AUTHORITY))
            raise ValueError(Notifications.REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR.format(ConfigKeys.AUTHENTICATION_TENANT_AUTHORITY))
        else:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.AUTHENTICATION_TENANT_AUTHORITY)

        if ConfigKeys.AUTHENTICATION_CLIENT_ID not in input_dictionary:
            logging.error(Notifications.REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR.format(ConfigKeys.AUTHENTICATION_CLIENT_ID))
            raise ValueError(Notifications.REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR.format(ConfigKeys.AUTHENTICATION_CLIENT_ID))
        else:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.AUTHENTICATION_CLIENT_ID)

        if ConfigKeys.START_DATE not in input_dictionary:
            input_dictionary[ConfigKeys.START_DATE] = datetime.now().date()
        else:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.START_DATE)
            cls.validate_input_is_date(input_dictionary, ConfigKeys.START_DATE)

        if ConfigKeys.END_DATE not in input_dictionary:
            input_dictionary[ConfigKeys.END_DATE] = datetime.now().date()
        else:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.END_DATE)
            cls.validate_input_is_date(input_dictionary, ConfigKeys.END_DATE)

        if ConfigKeys.COLUMN_TO_SEARCH in input_dictionary:
            cls.validate_input_is_string(input_dictionary, ConfigKeys.COLUMN_TO_SEARCH)

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

    @staticmethod
    def validate_input_is_date(input_dictionary, key):
        try:
            input_dictionary[key] = datetime.strptime(input_dictionary[key], '%m-%d-%Y').date()
        except ValueError:
            logging.error(Notifications.INVALID_DATE_FORMAT_ERROR.format(input_dictionary[key], key))
            raise ValueError(Notifications.INVALID_DATE_FORMAT_ERROR.format(input_dictionary[key], key))

import pandas
import logging
import hashlib
from inois.application_properties import *
from inois.utils.notifications import Notifications


class HashService:

    @classmethod
    def hash_files(cls, config):
        logging.info(Notifications.HASHING_FILES)
        print("\n" + Notifications.HASHING_FILES)
        for file in config.FILES:
            logging.info(Notifications.CURRENT_FILE.format(file))
            print(Notifications.CURRENT_FILE.format(file))
            data = cls.read_csv(file, config)
            cls.verify_columns_to_hash_exist(file, data, config)
            cls.hash_csv(file, data, config)
            cls.write_hashed_csv(file, data)

    @staticmethod
    def read_csv(file, config):
        logging.debug("reading file".format(file))
        try:
            return pandas.read_csv(file, delimiter=config.CSV_DELIMITER, dtype=object, encoding=DEFAULT_CSV_ENCODING)

        except pandas.errors.EmptyDataError:
            logging.error(Notifications.EMPTY_CSV_FILE_ERROR.format(file))
            raise ValueError(Notifications.EMPTY_CSV_FILE_ERROR.format(file))
        except UnicodeDecodeError:
            logging.error(Notifications.INVALID_CSV_FILE_FORMAT_ERROR.format(file, config.CSV_DELIMITER))
            raise TypeError(Notifications.INVALID_CSV_FILE_FORMAT_ERROR.format(file, config.CSV_DELIMITER))
        except ValueError:
            logging.error(Notifications.INVALID_CSV_FILE_FORMAT_ERROR.format(file, config.CSV_DELIMITER))
            raise TypeError(Notifications.INVALID_CSV_FILE_FORMAT_ERROR.format(file, config.CSV_DELIMITER))

    @staticmethod
    def verify_columns_to_hash_exist(file, data, config):
        logging.debug("verifying columns to hash exist")
        columns_in_csv = data.columns.values.tolist()
        for column_to_hash in config.COLUMNS_TO_HASH:
            if column_to_hash not in columns_in_csv:
                logging.error(Notifications.COLUMN_TO_HASH_NOT_FOUND_ERROR.format(column_to_hash, file, config.CSV_DELIMITER))
                raise ValueError(Notifications.COLUMN_TO_HASH_NOT_FOUND_ERROR.format(column_to_hash, file, config.CSV_DELIMITER))

    @classmethod
    def hash_csv(cls, file, data, config):
        logging.debug("hashing csv file {0}".format(file))
        for column_to_hash in config.COLUMNS_TO_HASH:
            data[column_to_hash + HASHED_FILE_EXTENSION] = data[column_to_hash].apply(cls.hash_value, args=("salt_key_placeholder",))

    @staticmethod
    def hash_value(value, salt):
        return hashlib.sha3_512(value.encode() + salt.encode()).hexdigest()

    @staticmethod
    def write_hashed_csv(file, data):
        logging.debug("writing hashed csv file {0}".format(file + HASHED_FILE_EXTENSION))
        data.to_csv(file[:-4] + HASHED_FILE_EXTENSION + ".csv", encoding=DEFAULT_CSV_ENCODING)
        #data.to_csv(file[:-4] + HASHED_FILE_EXTENSION + ".csv", encoding=DEFAULT_CSV_ENCODING, compression='gzip')
        logging.info(Notifications.HASHING_SUCCESSFUL.format(file[:-4] + HASHED_FILE_EXTENSION + ".csv"))
        print(Notifications.HASHING_SUCCESSFUL.format(file[:-4] + HASHED_FILE_EXTENSION + ".csv"))

import pandas
import logging
from inois.application_properties import *
from inois.models.config import Config
from inois.utils.notifications import Notifications


class HashService:

    @classmethod
    def hash_files(cls, config):
        logging.info("Hashing csv files...")
        for file in config.FILES:
            data = cls.read_csv(file, config)
            cls.verify_columns_to_hash_exist(file, data, config)
            cls.hash_csv(file, data)
            cls.write_hashed_csv(file, data)

    @staticmethod
    def read_csv(file, config):
        logging.debug("reading csv file {0}".format(file))
        try:
            return pandas.read_csv(file,
                                   delimiter=config.CSV_DELIMITER,
                                   dtype=object,
                                   encoding=DEFAULT_CSV_ENCODING)
        except pandas.errors.EmptyDataError:
            logging.error(Notifications.EMPTY_CSV_FILE_ERROR.format(file))
            raise ValueError(Notifications.EMPTY_CSV_FILE_ERROR.format(file))
        except UnicodeDecodeError:
            logging.error(Notifications.INVALID_CSV_FILE_FORMAT_ERROR.format(file))
            raise TypeError(Notifications.INVALID_CSV_FILE_FORMAT_ERROR.format(file))

    @staticmethod
    def verify_columns_to_hash_exist(file, data, config):
        logging.debug("verifying columns to hash exist".format(file))
        columns_in_csv = data.columns.values.tolist()
        print(columns_in_csv)
        for column_to_hash in config.COLUMNS_TO_HASH:
            if column_to_hash not in columns_in_csv:
                logging.error(Notifications.COLUMN_TO_HASH_NOT_FOUND_ERROR.format(column_to_hash, file))
                raise ValueError(Notifications.COLUMN_TO_HASH_NOT_FOUND_ERROR.format(column_to_hash, file))

    @staticmethod
    def hash_csv(file, data):
        logging.debug("hashing csv file {0}".format(file))

    @staticmethod
    def write_hashed_csv(file, data):
        logging.debug("writing hashed csv file {0}".format(file + HASHED_FILE_EXTENSION))

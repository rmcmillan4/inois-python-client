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
            cls.hash_csv(file, data)
            cls.write_hashed_csv(file, data)

    @staticmethod
    def read_csv(file, config):
        logging.debug("reading csv file {0}".format(file))
        data = pandas.read_csv()

    @staticmethod
    def hash_csv(file, data):
        logging.debug("hashing csv file {0}".format(file))

    @staticmethod
    def write_hashed_csv(file, data):
        logging.debug("writing hashed csv file {0}".format(file + HASHED_FILE_EXTENSION))

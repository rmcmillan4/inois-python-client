import pandas
import logging
import hashlib
from inois.application_properties import *
from inois.utils.notifications import Notifications
from inois.utils.api_keys import ApiKeys
import base64


class HashService:

    @classmethod
    def hash_files(cls, config, keys):
        logging.info(Notifications.CHUNKING_FILES)
        print("\n" + Notifications.CHUNKING_FILES)

        for file in config.FILES:
            logging.info(Notifications.CURRENT_FILE.format(file))
            print(Notifications.CURRENT_FILE.format(file))
            cls.chunk_file(file, config)

        logging.info(Notifications.HASHING_FILES)
        print("\n" + Notifications.HASHING_FILES)

        for file in config.CHUNKED_FILES:
            logging.info(Notifications.CURRENT_FILE.format(file))
            print(Notifications.CURRENT_FILE.format(file))
            data = cls.read_csv(file, config)
            cls.verify_columns_to_hash_exist(file, data, config)
            cls.hash_csv(file, data, config, keys)
            cls.write_hashed_csv(file, data, config)

    @classmethod
    def hash_records_for_search(cls, config, keys):
        logging.info(Notifications.HASHING_SEARCH_ENTRIES)
        print("\n" + Notifications.HASHING_SEARCH_ENTRIES)
        search_queries = {}
        for file in config.FILES:
            logging.info(Notifications.CURRENT_FILE.format(file))
            print(Notifications.CURRENT_FILE.format(file))
            data = cls.read_csv(file, config)
            cls.verify_column_to_search_exists(file, data, config)
            cls.hash_entries_for_search(search_queries, data, config, keys)
            logging.info(Notifications.HASHING_SEARCH_ENTRIES_SUCCESSFUL)
            print(Notifications.HASHING_SEARCH_ENTRIES_SUCCESSFUL.format(file))

        return search_queries

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

    @staticmethod
    def verify_column_to_search_exists(file, data, config):
        logging.debug("verifying column to search exists")
        columns_in_csv = data.columns.values.tolist()
        if config.COLUMN_TO_SEARCH not in columns_in_csv:
            logging.error(Notifications.COLUMN_TO_HASH_NOT_FOUND_ERROR.format(config.COLUMN_TO_SEARCH, file, config.CSV_DELIMITER))
            raise ValueError(Notifications.COLUMN_TO_HASH_NOT_FOUND_ERROR.format(config.COLUMN_TO_SEARCH, file, config.CSV_DELIMITER))

    @classmethod
    def hash_csv(cls, file, data, config, keys):
        logging.debug("hashing csv file {0}".format(file))
        for column_to_hash in config.COLUMNS_TO_HASH:
            data[column_to_hash + HASHED_FILE_EXTENSION] = data[column_to_hash].apply(cls.hash_value, args=(keys[ApiKeys.SALT_KEYS][0][ApiKeys.SALT_VALUE],))

        for column_to_hash in config.COLUMNS_TO_HASH:
            data[column_to_hash + PREVIOUS_HASH_COLUMN_EXTENSION] = data[column_to_hash].apply(cls.generate_previous_hashes, args=(keys[ApiKeys.SALT_KEYS],))

    @classmethod
    def hash_entries_for_search(cls, search_queries, data, config, keys):
        logging.debug("hashing input data to query")
        column_data = data[config.COLUMN_TO_SEARCH].tolist()
        for entry in column_data:
            hash_versions = []
            for salt_key in keys[ApiKeys.SALT_KEYS]:
                hash_versions.append(cls.hash_value(entry, salt_key[ApiKeys.SALT_VALUE]))
            search_queries[entry] = hash_versions

    @staticmethod
    def hash_value(value, salt):
        return hashlib.sha3_512(value.encode() + salt.encode()).hexdigest()

    @staticmethod
    def generate_previous_hashes(value, salts):
        previous_hash_string = ""
        if len(salts) == 1:
            return previous_hash_string
        for salt in salts[1:]:
            previous_hash_string += hashlib.sha3_512(value.encode() + salt[ApiKeys.SALT_VALUE].encode()).hexdigest() + " "

        return previous_hash_string

    @staticmethod
    def write_hashed_csv(file, data, config):
        logging.debug("writing hashed csv file {0}".format(file + HASHED_FILE_EXTENSION))
        data.to_csv(file[:-4] + HASHED_FILE_EXTENSION + ".csv", encoding=DEFAULT_CSV_ENCODING)
        config.HASHED_FILES.append(file[:-4] + HASHED_FILE_EXTENSION + ".csv")
        #data.to_csv(file[:-4] + HASHED_FILE_EXTENSION + ".csv.zip", encoding=DEFAULT_CSV_ENCODING, compression='zip')
        #config.HASHED_FILES.append(file[:-4] + HASHED_FILE_EXTENSION + ".csv.zip")
        logging.info(Notifications.HASHING_SUCCESSFUL.format(file[:-4] + HASHED_FILE_EXTENSION + ".csv"))
        print(Notifications.HASHING_SUCCESSFUL.format(file[:-4] + HASHED_FILE_EXTENSION + ".csv"))
        #
        # with open(file[:-4] + HASHED_FILE_EXTENSION + ".csv.zip", 'rb') as fin, open('output.zip.b64', 'wb') as fout:
        #     test = base64.b64encode(fin.read())
        #     fout.write(test)
        # print("success")

    @staticmethod
    def chunk_file(file, config):
        index = 1
        for chunk in pandas.read_csv(file, chunksize=CSV_FILE_CHUNK_SIZE):
            chunk.to_csv(file[:-4] + "_chunk_" + str(index) + ".csv", encoding=DEFAULT_CSV_ENCODING)
            config.CHUNKED_FILES.append(file[:-4] + "_chunk_" + str(index) + ".csv")
            index += 1

        logging.info(Notifications.CHUNKING_SUCCESSFUL.format(file, str(index - 1)))
        print(Notifications.CHUNKING_SUCCESSFUL.format(file, str(index - 1)))



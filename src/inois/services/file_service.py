import os
import logging
import glob
from inois.utils.notifications import Notifications


class FileService:

    @classmethod
    def validate_files(cls, config):
        logging.info("Validating Files...")
        cls.navigate_to_working_directory(config)
        cls.validate_csv_file_extensions(config)
        cls.validate_files_exist(config)

    @staticmethod
    def navigate_to_working_directory(config):
        logging.debug("navigating to working directory")
        if not os.path.exists(config.WORKING_DIRECTORY):
            logging.error(Notifications.DIRECTORY_NOT_FOUND_ERROR.format(config.WORKING_DIRECTORY))
            raise OSError(Notifications.DIRECTORY_NOT_FOUND_ERROR.format(config.WORKING_DIRECTORY))
        os.chdir(config.WORKING_DIRECTORY)
        config.WORKING_DIRECTORY = os.path.realpath(os.getcwd())
        logging.info(Notifications.ACTIVE_WORKING_DIRECTORY.format(config.WORKING_DIRECTORY))
        print(Notifications.ACTIVE_WORKING_DIRECTORY.format(config.WORKING_DIRECTORY))

    @staticmethod
    def validate_csv_file_extensions(config):
        logging.debug("validating csv file extensions")
        if "*" not in config.FILES:
            for file in config.FILES:
                if not file[-4:] == ".csv":
                    logging.error((Notifications.NON_CSV_FILE_EXTENSION_ERROR.format(file)))
                    raise TypeError(Notifications.NON_CSV_FILE_EXTENSION_ERROR.format(file))

    @classmethod
    def validate_files_exist(cls, config):
        logging.debug("validating files exist")
        if "*" in config.FILES:
            cls.find_all_csv_files_in_working_directory(config)
        else:
            cls.locate_csv_files_from_config(config)

    @staticmethod
    def find_all_csv_files_in_working_directory(config):
        config.FILES = glob.glob("*.csv")
        if len(config.FILES) == 0:
            logging.error(Notifications.NO_CSV_FILES_FOUND_IN_FOLDER_ERROR.format(config.WORKING_DIRECTORY))
            raise FileNotFoundError(Notifications.NO_CSV_FILES_FOUND_IN_FOLDER_ERROR.format(config.WORKING_DIRECTORY))

        for file in config.FILES:
            logging.info(Notifications.FILE_FOUND.format(os.path.join(config.WORKING_DIRECTORY, file)))
            print(Notifications.FILE_FOUND.format(os.path.join(config.WORKING_DIRECTORY, file)))

    @staticmethod
    def locate_csv_files_from_config(config):
        for file in config.FILES:
            if not os.path.exists(os.path.join(config.WORKING_DIRECTORY, file)):
                logging.error(Notifications.FILE_NOT_FOUND_ERROR.format(os.path.join(config.WORKING_DIRECTORY, file)))
                raise FileNotFoundError(
                    Notifications.FILE_NOT_FOUND_ERROR.format(os.path.join(config.WORKING_DIRECTORY, file)))
            else:
                logging.info(Notifications.FILE_FOUND.format(os.path.join(config.WORKING_DIRECTORY, file)))
                print(Notifications.FILE_FOUND.format(os.path.join(config.WORKING_DIRECTORY, file)))

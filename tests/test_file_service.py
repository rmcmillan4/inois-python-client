import pytest
import os
import glob
from inois.services.config_service import ConfigService
from inois.services.file_service import FileService
from inois.application_properties import *


class TestFileServiceClass:
    test_directory = os.path.realpath(os.getcwd())

    def test_navgiate_to_working_directory_with_nonexistant_directory(self):
        with pytest.raises(OSError):
            config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
            config.WORKING_DIRECTORY = config.WORKING_DIRECTORY+'^&(^&(^&*('
            FileService.navigate_to_working_directory(config)

    def test_navgiate_to_working_directory_with_valid_directory(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        previous_directory = os.path.realpath(os.getcwd())
        FileService.navigate_to_working_directory(config)
        assert config.WORKING_DIRECTORY == os.getcwd()
        os.chdir(previous_directory)

    def test_validate_csv_file_extensions_with_invalid_extensions(self):
        with pytest.raises(TypeError):
            config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
            config.FILES = config.FILES.append("file.xls")
            FileService.navigate_to_working_directory(config)
            FileService.validate_csv_file_extensions(config)

    def test_validate_csv_file_extensions_with_valid_extensions(self):
        os.chdir(self.test_directory)
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        FileService.navigate_to_working_directory(config)
        FileService.validate_csv_file_extensions(config)
        for file in config.FILES:
            assert file[-4:] == ".csv"

    def test_validate_files_exist_with_nonexistant_file(self):
        with pytest.raises(FileNotFoundError):
            os.chdir(self.test_directory)
            config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
            config.WORKING_DIRECTORY = "tests"
            FileService.navigate_to_working_directory(config)
            FileService.validate_csv_file_extensions(config)
            FileService.validate_files_exist(config)

    def test_validate_files_exist_with_no_csv_file_in_directory(self):
        with pytest.raises(FileNotFoundError):
            os.chdir(self.test_directory)
            config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
            config.FILES = ["*"]
            config.WORKING_DIRECTORY = "tests"
            FileService.navigate_to_working_directory(config)
            FileService.validate_csv_file_extensions(config)
            FileService.validate_files_exist(config)

    def test_validate_files_exist_with_existing_file(self):
        os.chdir(self.test_directory)
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        FileService.navigate_to_working_directory(config)
        FileService.validate_csv_file_extensions(config)
        FileService.validate_files_exist(config)
        file_instance = glob.glob(config.FILES[0])
        assert len(file_instance) > 0

    def test_validate_files_exist_with_csv_file_in_directory(self):
        os.chdir(self.test_directory)
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        config.FILES = ["*"]
        FileService.navigate_to_working_directory(config)
        FileService.validate_csv_file_extensions(config)
        FileService.validate_files_exist(config)
        file_instance = glob.glob("*.csv")
        assert len(file_instance) > 0

    def test_validate_files(self):
        os.chdir(self.test_directory)
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        FileService.validate_files(config)
        if "*" in config.FILES:
            for file in config.FILES:
                assert file in glob.glob("*.csv")





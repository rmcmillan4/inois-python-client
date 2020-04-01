import pytest
import os
import pandas
from inois.application_properties import *
from inois.services.config_service import ConfigService
from inois.services.hash_service import HashService


class TestHashServiceClass:
    config = ConfigService.initialize_config('tests/utils/config_example.txt')

    def test_read_csv_with_valid_csv_file(self):
        HashService.read_csv(self.config.FILES[0], self.config)

    def test_read_csv_with_empty_csv_file(self):
        with pytest.raises(ValueError):
            self.config.FILES = ['empty_file.csv']
            HashService.read_csv(self.config.FILES[0], self.config)

    def test_read_csv_with_non_csv_file(self):
        with pytest.raises(TypeError):
            self.config.FILES = ['png_image_file.csv']
            HashService.read_csv(self.config.FILES[0], self.config)

    def test_read_csv_with_empty_csv_delimiter(self):
        with pytest.raises(TypeError):
            self.config.FILES = ['example_inois_data.csv']
            self.config.CSV_DELIMITER = ''
            HashService.read_csv(self.config.FILES[0], self.config)

    def test_verify_columns_to_hash_exist_with_valid_column(self):
        self.config.CSV_DELIMITER = ','
        file_data = HashService.read_csv(self.config.FILES[0], self.config)
        HashService.verify_columns_to_hash_exist(self.config.FILES[0], file_data, self.config)

    def test_verify_columns_to_hash_exist_with_invalid_column(self):
        with pytest.raises(ValueError):
            self.config.COLUMNS_TO_HASH = ["Bad-Column"]
            file_data = HashService.read_csv(self.config.FILES[0], self.config)
            HashService.verify_columns_to_hash_exist(self.config.FILES[0], file_data, self.config)

    def test_hash_csv_with_valid_input(self):
        self.config.COLUMNS_TO_HASH = ['SSN']
        file_data = HashService.read_csv(self.config.FILES[0], self.config)
        HashService.hash_csv(self.config.FILES[0], file_data, self.config)

    def test_hash_value(self):
        value = "123456789"
        identical_value = "123456789"
        salt_key = "vhjkwfeho178348"
        hashed_value = HashService.hash_value(value, salt_key)
        hashed_identical_value = HashService.hash_value(identical_value, salt_key)
        assert value == identical_value
        assert value != hashed_value
        assert hashed_value == hashed_identical_value

    def test_write_hashed_csv_with_valid_input(self):
        file_data = HashService.read_csv(self.config.FILES[0], self.config)
        HashService.hash_csv(self.config.FILES[0], file_data, self.config)
        HashService.write_hashed_csv(self.config.FILES[0], file_data)
        assert os.path.exists(self.config.FILES[0][:-4] + HASHED_FILE_EXTENSION + ".csv")
        os.remove(self.config.FILES[0][:-4] + HASHED_FILE_EXTENSION + ".csv")

    def test_hash_files(self):
        HashService.hash_files(self.config)
        input_csv = pandas.read_csv(self.config.FILES[0], delimiter=self.config.CSV_DELIMITER, dtype=object, encoding=DEFAULT_CSV_ENCODING)
        hashed_csv_file_name = self.config.FILES[0][:-4] + HASHED_FILE_EXTENSION + ".csv"
        hashed_csv = pandas.read_csv(hashed_csv_file_name, delimiter=self.config.CSV_DELIMITER, dtype=object, encoding=DEFAULT_CSV_ENCODING)
        input_csv_columns = input_csv.columns.values.tolist()
        hashed_csv_columns = hashed_csv.columns.values.tolist()
        for column in input_csv_columns:
            if column not in self.config.COLUMNS_TO_HASH:
                assert column in hashed_csv_columns
                assert input_csv[column][0] == hashed_csv[column][0]
            else:
                assert column + HASHED_FILE_EXTENSION in hashed_csv_columns
                assert input_csv[column][0] != hashed_csv[column + HASHED_FILE_EXTENSION][0]

        os.remove(self.config.FILES[0][:-4] + HASHED_FILE_EXTENSION + ".csv")



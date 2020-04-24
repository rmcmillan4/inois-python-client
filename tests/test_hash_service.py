import pytest
import os
import pandas
from inois.application_properties import *
from inois.services.config_service import ConfigService
from inois.services.hash_service import HashService
from inois.utils.api_keys import ApiKeys


class TestHashServiceClass:
    config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)

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
        mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}], ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
        file_data = HashService.read_csv(self.config.FILES[0], self.config)
        HashService.hash_csv(self.config.FILES[0], file_data, self.config, mock_keys)

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
        mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}], ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
        HashService.hash_csv(self.config.FILES[0], file_data, self.config, mock_keys)
        HashService.write_hashed_csv(self.config.FILES[0], file_data, self.config)
        assert os.path.exists(self.config.HASHED_FILES[0])
        os.remove(self.config.HASHED_FILES[0])

    def test_hash_files(self):
        mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}], ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
        HashService.hash_files(self.config, mock_keys)
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

        os.remove(self.config.HASHED_FILES[0])

    def test_hash_records_for_search(self):
        mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}], ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
        search_queries = HashService.hash_records_for_search(self.config, mock_keys)
        assert search_queries.keys() is not None
        for key in search_queries:
            assert isinstance(search_queries[key], list)
            assert isinstance(search_queries[key][0], str)



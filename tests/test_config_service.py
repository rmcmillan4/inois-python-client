import pytest
from inois.utils.config_keys import ConfigKeys
from inois.services.config_service import ConfigService
from inois.application_properties import *


class TestConfigServiceClass:

    def test_read_input_with_nonexistant_file(self):
        with pytest.raises(FileNotFoundError):
            ConfigService.read_input('invalid_file_path')

    def test_read_input_with_invalid_file_format(self):
        with pytest.raises(TypeError):
            ConfigService.read_input('tests/utils/example_inois_data.csv')

    def test_read_input_with_valid_file_format(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        assert isinstance(config, dict)

    def test_validate_input_with_invalid_key(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config['INVALID_KEY'] = True
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_validate_input_with_invalid_working_directory_value(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config[ConfigKeys.WORKING_DIRECTORY] = 0
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_validate_input_with_invalid_csv_delimiter_value(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config[ConfigKeys.CSV_DELIMITER] = 9
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_validate_input_with_invalid_files_value(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config[ConfigKeys.FILES] = ('tests/utils/config_example.txt', )
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_validate_input_with_invalid_file_item_value(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config[ConfigKeys.FILES] = ['tests/utils/config_example.txt', 9]
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_validate_input_with_invalid_columns_value(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config[ConfigKeys.COLUMNS_TO_HASH] = 9
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_validate_input_with_invalid_column_item_value(self):
        config = ConfigService.read_input('tests/utils/config_example.txt')
        config[ConfigKeys.COLUMNS_TO_HASH] = [None]
        with pytest.raises(ValueError):
            ConfigService.validate_input(config)

    def test_set_config(self):
        config_dictionary = ConfigService.read_input('tests/utils/config_example.txt')
        ConfigService.validate_input(config_dictionary)
        config = ConfigService.set_config(config_dictionary)
        assert config.WORKING_DIRECTORY == config_dictionary[ConfigKeys.WORKING_DIRECTORY] or config.WORKING_DIRECTORY == DEFAULT_WORKING_DIRECTORY
        assert config.FILES == config_dictionary[ConfigKeys.FILES] or config.FILES == ['*']
        assert config.COLUMNS_TO_HASH == config_dictionary[ConfigKeys.COLUMNS_TO_HASH] or config.COLUMNS_TO_HASH == DEFAULT_COLUMNS_TO_HASH
        assert config.CSV_DELIMITER == config_dictionary[ConfigKeys.CSV_DELIMITER] or config.CSV_DELIMITER is DEFAULT_CSV_DELIMiTER

    def test_initialize_config(self):
        config = ConfigService.initialize_config('tests/utils/config_example.txt')
        assert isinstance(config.WORKING_DIRECTORY, str)
        assert isinstance(config.FILES, list)
        assert isinstance(config.FILES[0], str)
        assert isinstance(config.COLUMNS_TO_HASH, list)
        assert isinstance(config.COLUMNS_TO_HASH[0], str)
        assert isinstance(config.CSV_DELIMITER, str)

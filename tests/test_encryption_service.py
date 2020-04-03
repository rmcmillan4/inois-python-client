import os
from inois.services.config_service import ConfigService
from inois.services.hash_service import HashService
from inois.services.encryption_service import EncryptionService
from inois.services.file_service import FileService
from inois.application_properties import *


class TestEncryptionServiceClass:
    test_directory = os.path.realpath(os.getcwd())

    def test_encrypt_files(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        FileService.validate_files(config)
        HashService.hash_files(config)
        EncryptionService.encrypt_files(config)
        assert len(config.ENCRYPTED_FILES) > 0
        os.remove(config.ENCRYPTED_FILES[0])
        os.remove(config.HASHED_FILES[0])
        os.chdir(self.test_directory)

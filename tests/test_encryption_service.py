import os
from inois.services.config_service import ConfigService
from inois.services.hash_service import HashService
from inois.services.encryption_service import EncryptionService
from inois.services.file_service import FileService
from inois.application_properties import *
from inois.utils.api_keys import ApiKeys


class TestEncryptionServiceClass:
    test_directory = os.path.realpath(os.getcwd())

    def test_encrypt_files(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}], ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
        FileService.validate_files(config)
        HashService.hash_files(config, mock_keys)
        EncryptionService.encrypt_files(config, mock_keys)
        assert len(config.ENCRYPTED_FILES) > 0
        os.remove(config.ENCRYPTED_FILES[0])
        os.remove(config.HASHED_FILES[0])
        os.chdir(self.test_directory)

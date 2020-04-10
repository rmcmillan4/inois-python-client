import os
from inois.services.config_service import ConfigService
import pytest
from inois.services.upload_service import UploadService
from inois.application_properties import *


class TestUploadServiceClass:
    test_directory = os.path.realpath(os.getcwd())
    config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)

    def test_upload_files_without_authorization(self):
        with pytest.raises(RuntimeError):
            os.chdir(self.test_directory)
            self.config.ENCRYPTED_FILES = [TEST_DATA_FILE_PATH]
            mock_sessipn = {'access_token': '6798697698'}
            UploadService.upload_files(self.config, mock_sessipn)

import os
from inois.services.config_service import ConfigService
import pytest
from inois.services.key_service import KeyService
from inois.application_properties import *
from inois.utils.api_keys import ApiKeys


class TestKeyServiceClass:
    test_directory = os.path.realpath(os.getcwd())
    config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)

    def test_validate_api_response_with_valid_response(self):
        mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}],
                     ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
        KeyService.validate_api_response(mock_keys, self.config)

    def test_validate_api_response_with_no_salt_keys(self):
        with pytest.raises(RuntimeError):
            mock_keys = {ApiKeys.SALT_KEYS: [], ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
            KeyService.validate_api_response(mock_keys, self.config)

    def test_validate_api_response_with_no_empty_keys(self):
        with pytest.raises(RuntimeError):
            mock_keys = {ApiKeys.ENCRYPTION_KEY: "_hSmVyMTLi-Qo_rmISp8jrH5Aob7frHp1X-28sxQZAU="}
            KeyService.validate_api_response(mock_keys, self.config)

    def test_validate_api_response_with_no_encryption_key(self):
        with pytest.raises(RuntimeError):
            mock_keys = {ApiKeys.SALT_KEYS: [{"value": "test-salt-key"}]}
            KeyService.validate_api_response(mock_keys, self.config)

    def test_get_keys_without_authorization(self):
        with pytest.raises(RuntimeError):
            mock_sessipn = {'access_token': '6798697698'}
            KeyService.get_keys(self.config, mock_sessipn)

from inois.services.authentication_service import AuthenticationService
from inois.services.config_service import ConfigService
from inois.application_properties import *


class TestAuthenticationServiceClass:

    def test_credentials_exist_in_config(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        assert config.AUTHENTICATION_TENANT_AUTHORITY is not None
        assert config.AUTHENTICATION_SCOPE is not None
        assert config.AUTHENTICATION_CLIENT_ID is not None

    def test_initialize_cache(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        authentication_service = AuthenticationService(config)
        authentication_service.initialize_cache()
        assert authentication_service.cache is not None

    def test_initialize_app_instance(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        authentication_service = AuthenticationService(config)
        authentication_service.initialize_cache()
        authentication_service.initialize_app_instance()
        assert authentication_service.app_instance is not None

    def test_initialize_session_from_cache(self):
        config = ConfigService.initialize_config(TEST_CONFIG_FILE_PATH)
        authentication_service = AuthenticationService(config)
        authentication_service.initialize_cache()
        authentication_service.initialize_app_instance()
        authentication_service.initialize_session_from_cache()
        if authentication_service.app_instance.get_accounts():
            pass
        else:
            assert authentication_service.session is None

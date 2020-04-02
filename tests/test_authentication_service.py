import os
from inois.services.authentication_service import AuthenticationService


class TestAuthenticationServiceClass:

    def test_credentials_exist_as_env_variables(self):
        AUTHENTICATION_TENANT_AUTHORITY = os.environ['AUTHENTICATION_TENANT_AUTHORITY']
        AUTHENTICATION_CLIENT_ID = os.environ['AUTHENTICATION_CLIENT_ID']
        AUTHENTICATION_SCOPE = [os.environ['AUTHENTICATION_SCOPE']]
        assert AUTHENTICATION_TENANT_AUTHORITY is not None
        assert AUTHENTICATION_SCOPE is not None
        assert AUTHENTICATION_CLIENT_ID is not None

    def test_initialize_cache(self):
        authentication_service = AuthenticationService()
        authentication_service.initialize_cache()
        assert authentication_service.cache is not None

    def test_initialize_app_instance(self):
        authentication_service = AuthenticationService()
        authentication_service.initialize_cache()
        authentication_service.initialize_app_instance()
        assert authentication_service.app_instance is not None

    def test_initialize_session_from_cache(self):
        authentication_service = AuthenticationService()
        authentication_service.initialize_cache()
        authentication_service.initialize_app_instance()
        authentication_service.initialize_session_from_cache()
        if authentication_service.app_instance.get_accounts():
            assert authentication_service.session is not None
        else:
            assert authentication_service.session is None
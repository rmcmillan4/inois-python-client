import sys
import json
import logging
import atexit
import os
import msal
from inois.application_properties import *
from inois.utils.notifications import Notifications


class AuthenticationService:

    def __init__(self):
        self.cache = msal.SerializableTokenCache()
        self.app_instance = None
        self.session = None

    def initialize_cache(self):
        logging.debug("initializing authentication cache")
        if os.path.exists("session_cache.bin"):
            self.cache.deserialize(open("session_cache.bin", "r").read())

        atexit.register(lambda: open("session_cache.bin", "w").write(self.cache.serialize()))

    def initialize_app_instance(self):
        logging.debug("initializing app instance")
        self.app_instance = msal.PublicClientApplication(AUTHENTICATION_CLIENT_ID, authority=AUTHENTICATION_TENANT_AUTHORITY, token_cache=self.cache)

    def initialize_session_from_cache(self):
        logging.debug("attempt to authenticate session from cache")
        user_accounts = self.app_instance.get_accounts()
        if user_accounts:
            logging.info(Notifications.PREVIOUS_SESSION_IN_CACHE)
            print(Notifications.PREVIOUS_SESSION_IN_CACHE)
            self.session = self.app_instance.acquire_token_silent(AUTHENTICATION_SCOPE, account=user_accounts[0])

    def initialize_session_from_login(self):
        logging.info(Notifications.AUTHENTICATION_REQUIRED)
        print(Notifications.AUTHENTICATION_REQUIRED)

        device_flow = self.app_instance.initiate_device_flow(scopes=AUTHENTICATION_SCOPE)
        if "user_code" not in device_flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(device_flow, indent=4))

        print(device_flow["message"])
        sys.stdout.flush()
        self.session = self.app_instance.acquire_token_by_device_flow(device_flow)

    def get_authorization(self):
        logging.info("obtaining authorization")
        self.initialize_cache()
        self.initialize_app_instance()
        self.initialize_session_from_cache()
        if not self.session:
            self.initialize_session_from_login()
        logging.info(Notifications.AUTHENTICATION_SUCCESSFUL)
        print(Notifications.AUTHENTICATION_SUCCESSFUL + "\n")
        return self.session


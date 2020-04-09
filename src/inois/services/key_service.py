from inois.application_properties import *
from inois.utils.notifications import Notifications
from inois.utils.api_keys import ApiKeys
import requests
import logging


class KeyService:

    @classmethod
    def get_keys(cls, config, session):
        logging.info(Notifications.FETCHING_API_KEYS)
        print("\n" + Notifications.FETCHING_API_KEYS)
        api_response = requests.get(INOIS_API_URL + INOIS_API_KEY_SERVICE_ROUTE, headers={'Authorization': 'Bearer ' + session['access_token']}, )

        if api_response:
            cls.validate_api_response(api_response.json(), config)
            return api_response.json()

        else:
            logging.error(Notifications.API_KEY_FETCH_ERROR.format(api_response.status_code))
            raise RuntimeError(Notifications.API_KEY_FETCH_ERROR.format(api_response.status_code))

    @staticmethod
    def validate_api_response(response, config):
        logging.debug("validating security keys from api response")

        if ApiKeys.SALT_KEYS not in response:
            logging.error(Notifications.API_KEY_FETCH_RESPONSE_FORMAT_ERROR.format(ApiKeys.SALT_KEYS))
            raise RuntimeError(Notifications.API_KEY_FETCH_RESPONSE_FORMAT_ERROR.format(ApiKeys.SALT_KEYS))

        if ApiKeys.ENCRYPTION_KEY not in response:
            logging.error(Notifications.API_KEY_FETCH_RESPONSE_FORMAT_ERROR.format(ApiKeys.ENCRYPTION_KEY))
            raise RuntimeError(Notifications.API_KEY_FETCH_RESPONSE_FORMAT_ERROR.format(ApiKeys.ENCRYPTION_KEY))

        if len(response[ApiKeys.SALT_KEYS]) == 0:
            logging.error(Notifications.EMPTY_SALT_KEY_ERROR)
            raise RuntimeError(Notifications.EMPTY_SALT_KEY_ERROR)

        logging.info(Notifications.API_KEY_FETCH_SUCCESSFUL)
        print(Notifications.API_KEY_FETCH_SUCCESSFUL)



from inois.application_properties import *
from inois.utils.notifications import Notifications
import requests
import logging


class UploadService:

    @classmethod
    def upload_files(cls, config, session):
        logging.info(Notifications.UPLOADING_FILES)
        print("\n" + Notifications.UPLOADING_FILES)

        for file in config.ENCRYPTED_FILES:
            cls.upload_file(file, session)

    @staticmethod
    def upload_file(file, session):
        logging.info(Notifications.CURRENT_FILE.format(file))
        print(Notifications.CURRENT_FILE.format(file))

        with open(file, 'rb') as file_content:
            api_response = requests.post(
                INOIS_API_URL + INOIS_API_UPLOAD_URL,
                headers={'Authorization': 'Bearer ' + session['access_token']},
                files={'file': file_content}
            )

        if not api_response:
            logging.error(Notifications.FILE_UPLOAD_FAILED.format(file, api_response.status_code))
            raise RuntimeError(Notifications.FILE_UPLOAD_FAILED.format(file, api_response.status_code))

        logging.info(Notifications.FILE_SUCCESSFULLY_UPLOADED.format(file, api_response.text[12:-2]))
        print(Notifications.FILE_SUCCESSFULLY_UPLOADED.format(file, api_response.text[12:-2]))



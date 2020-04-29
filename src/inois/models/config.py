from inois.utils.config_keys import ConfigKeys
from inois.application_properties import *
import os


class Config:

    def __init__(self, settings):
        self.LAUNCH_DIRECTORY = os.path.realpath(os.getcwd())
        self.WORKING_DIRECTORY = settings.get(ConfigKeys.WORKING_DIRECTORY, DEFAULT_WORKING_DIRECTORY)
        self.FILES = settings.get(ConfigKeys.FILES, DEFAULT_FILES_TO_HASH)
        self.COLUMNS_TO_HASH = settings.get(ConfigKeys.COLUMNS_TO_HASH, DEFAULT_COLUMNS_TO_HASH)
        self.CSV_DELIMITER = DEFAULT_CSV_DELIMITER
        self.AUTHENTICATION_CLIENT_ID = settings.get(ConfigKeys.AUTHENTICATION_CLIENT_ID, None)
        self.AUTHENTICATION_TENANT_AUTHORITY = settings.get(ConfigKeys.AUTHENTICATION_TENANT_AUTHORITY, None)
        self.AUTHENTICATION_SCOPE = settings.get(ConfigKeys.AUTHENTICATION_SCOPE, None)
        self.HASHED_FILES = []
        self.ENCRYPTED_FILES = []
        self.START_DATE = settings.get(ConfigKeys.START_DATE, None)
        self.END_DATE = settings.get(ConfigKeys.END_DATE, None)
        self.COLUMN_TO_SEARCH = settings.get(ConfigKeys.COLUMN_TO_SEARCH, None)
        self.CHUNKED_FILES = []

    def __str__(self):
        return """
---Config Settings---
Working Directory: '{0}'
Files to Hash: {1}
Columns to Hash: {2}
CSV Delimiter: '{3}'
Column to Search: '{4}'
Data Start Date: '{5}'
Data End Date: '{5}'
---------------------
        """.format(self.WORKING_DIRECTORY, self.FILES, self.COLUMNS_TO_HASH,
                   self.CSV_DELIMITER, self.COLUMN_TO_SEARCH, self.START_DATE,
                   self.END_DATE)

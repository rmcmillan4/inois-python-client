from inois.utils.config_keys import ConfigKeys
from inois.application_properties import *


class Config:

    def __init__(self, settings):
        self.WORKING_DIRECTORY = settings.get(ConfigKeys.WORKING_DIRECTORY, DEFAULT_WORKING_DIRECTORY)
        self.FILES = settings.get(ConfigKeys.FILES, DEFAULT_FILES_TO_HASH)
        self.COLUMNS_TO_HASH = settings.get(ConfigKeys.COLUMNS_TO_HASH, DEFAULT_COLUMNS_TO_HASH)
        self.CSV_DELIMITER = settings.get(ConfigKeys.CSV_DELIMITER, DEFAULT_CSV_DELIMiTER)

    def __str__(self):
        return """
---Config Settings---
Working Directory: '{0}',
Files to Hash: {1},
Columns to Hash: {2}
CSV Delimiter: '{3}'
---------------------
        """.format(self.WORKING_DIRECTORY, self.FILES, self.COLUMNS_TO_HASH, self.CSV_DELIMITER)

from inois.utils.config_keys import ConfigKeys


class Config:

    def __init__(self, settings):
        self.WORKING_DIRECTORY = settings.get(ConfigKeys.WORKING_DIRECTORY, ".")
        self.FILES = settings.get(ConfigKeys.FILES, ["*"])
        self.COLUMNS_TO_HASH = settings.get(ConfigKeys.COLUMNS_TO_HASH, ["ssn"])
        self.USERNAME = settings.get(ConfigKeys.USERNAME, None)

    def __str__(self):
        return """
    Config Settings...
    Working Directory: {0},
    Files to Hash: {1},
    Columns to Hash: {2}
        """.format(self.WORKING_DIRECTORY, self.FILES, self.COLUMNS_TO_HASH)

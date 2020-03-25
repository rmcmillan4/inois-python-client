class Config:
    KEYS = ("working_directory", "files", "columns_to_hash", "username")

    def __init__(self, settings):
        self.WORKING_DIRECTORY = settings.get(Config.KEYS[0], ".")
        self.FILES = settings.get(Config.KEYS[1], ["*"])
        self.COLUMNS_TO_HASH = settings.get(Config.KEYS[2], ["ssn"])
        self.USERNAME = settings.get(Config.KEYS[2], None)

    def __str__(self):
        return """
    Config Settings...
    Working Directory: {0},
    Files to Hash: {1},
    Columns to Hash: {2}
        """.format(self.WORKING_DIRECTORY, self.FILES, self.COLUMNS_TO_HASH)

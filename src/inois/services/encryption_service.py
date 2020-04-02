import logging
from cryptography.fernet import Fernet
from inois.utils.notifications import Notifications


class EncryptionService:

    @classmethod
    def encrypt_files(cls, config, key=Fernet.generate_key()):
        logging.info(Notifications.ENCRYPTING_FILES)
        print("\n" + Notifications.ENCRYPTING_FILES)
        for file in config.HASHED_FILES:
            cls.encrypt_hashed_csv_file(file, key, config)

    @staticmethod
    def encrypt_hashed_csv_file(file, key, config):
        logging.info(Notifications.CURRENT_FILE.format(file))
        print(Notifications.CURRENT_FILE.format(file))
        with open(file, 'rb') as hashed_csv:
            data = hashed_csv.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        with open(file + ".enc", 'wb') as encrypted_csv:
            encrypted_csv.write(encrypted_data)

        config.ENCRYPTED_FILES.append(file + ".enc")
        logging.info(Notifications.ENCRYPTION_SUCCESSFUL.format(file + ".enc"))
        print(Notifications.ENCRYPTION_SUCCESSFUL.format(file + ".enc"))

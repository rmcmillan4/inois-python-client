import click
import logging
import os
from inois.utils.banner import Banner
from inois.services.config_service import ConfigService
from inois.services.file_service import FileService
from inois.services.hash_service import HashService
from inois.services.authentication_service import AuthenticationService
from inois.services.encryption_service import EncryptionService
from inois.services.key_service import KeyService
from inois import __version__

__author__ = "Robert MacMillan"
__copyright__ = "GSU"
__license__ = "mit"


@click.command()
@click.option('--log_file', default=None, help='Location to write log file.')
@click.option('--input_file', prompt='input file', help='Path to the INOIS input configuration file.')
def run(input_file, log_file):
    """Entry point for the inois hashing application."""

    log_level = logging.DEBUG if log_file else logging.CRITICAL
    log_location = log_file if log_file else "inois.log"
    logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s', filename=log_location, level=log_level)

    logging.info("Application Started")
    print(Banner.TEXT)
    config = ConfigService.initialize_config(input_file=input_file)
    session = AuthenticationService(config).get_authorization()
    FileService.validate_files(config)
    keys = KeyService.get_keys(config, session)
    #print(keys)
    HashService.hash_files(config)
    EncryptionService.encrypt_files(config)
    os.chdir(config.LAUNCH_DIRECTORY)


if __name__ == "__main__":
    run()

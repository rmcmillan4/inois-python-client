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
from inois.services.upload_service import UploadService
from inois.utils.application_mode_keys import ApplicationModeKeys
from inois import __version__

__author__ = "Robert MacMillan"
__copyright__ = "GSU"
__license__ = "mit"


@click.command()
@click.option('--log_file', default=None, help='Location to write log file.')
@click.option('--input_file', prompt='input file', help='Path to the INOIS input configuration file.')
@click.option('--mode', prompt='application mode (enter "upload" or "search")', help='Run the application in record upload or record search mode.')
def run(input_file, log_file, mode):
    """Entry point for the inois hashing application."""

    log_level = logging.DEBUG if log_file else logging.CRITICAL
    log_location = log_file if log_file else "inois.log"
    logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s', filename=log_location, level=log_level)
    application_mode = mode if mode == ApplicationModeKeys.SEARCH else ApplicationModeKeys.UPLOAD
    logging.info("Application Started in '{0}' mode".format(application_mode))
    print(Banner.TEXT)

    config = ConfigService.initialize_config(input_file=input_file)
    session = AuthenticationService(config).get_authorization()
    print(session['access_token'])
    FileService.validate_files(config)

    if application_mode == ApplicationModeKeys.UPLOAD:
        keys = KeyService.get_keys(config, session)
        HashService.hash_files(config, keys)
        EncryptionService.encrypt_files(config, keys)
        UploadService.upload_files(config, session)
        os.chdir(config.LAUNCH_DIRECTORY)

    elif application_mode == ApplicationModeKeys.SEARCH:
        print("Search Mode Active")


if __name__ == "__main__":
    run()

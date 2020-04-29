import click
import logging
import os
from datetime import datetime
from inois.utils.banner import Banner
from inois.services.config_service import ConfigService
from inois.services.file_service import FileService
from inois.services.hash_service import HashService
from inois.services.authentication_service import AuthenticationService
from inois.services.encryption_service import EncryptionService
from inois.services.key_service import KeyService
from inois.services.upload_service import UploadService
from inois.services.search_service import SearchService
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
    """Entry point for the INOIS application."""

    log_level = logging.DEBUG if log_file else logging.CRITICAL
    log_location = log_file if log_file else "inois.log"
    logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s', filename=log_location, level=log_level)

    application_mode = mode if mode == ApplicationModeKeys.SEARCH else ApplicationModeKeys.UPLOAD

    logging.info("INOIS application Started in '{0}' mode at {1}".format(application_mode, datetime.now()))
    print("INOIS application Started in '{0}' mode at {1}".format(application_mode, datetime.now()))
    print(Banner.TEXT)
    config = ConfigService.initialize_config(input_file=input_file)
    session = AuthenticationService(config).get_authorization()
    #print(session['access_token'])
    FileService.validate_files(config)
    keys = KeyService.get_keys(config, session)

    if application_mode == ApplicationModeKeys.UPLOAD:
        HashService.hash_files(config, keys)
        EncryptionService.encrypt_files(config, keys)
        UploadService.upload_files(config, session)

    elif application_mode == ApplicationModeKeys.SEARCH:
        search_queries = HashService.hash_records_for_search(config, keys)
        SearchService.search_on_all_queries(search_queries, session)

    os.chdir(config.LAUNCH_DIRECTORY)
    logging.info("INOIS application terminated successfully at {0}".format(datetime.now()))
    print("\nINOIS application terminated successfully at {0}".format(datetime.now()))


if __name__ == "__main__":
    run()

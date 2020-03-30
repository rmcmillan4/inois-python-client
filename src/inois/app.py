import click
import logging
from inois.utils.banner import Banner
from inois.services.config_service import ConfigService
from inois.services.file_service import FileService
from inois.services.hash_service import HashService
from inois import __version__

__author__ = "Robert MacMillan"
__copyright__ = "GSU"
__license__ = "mit"
# _logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s', filename='inois.log', level=logging.DEBUG)


@click.command()
@click.option('--input_file', prompt='input file', help='Path to the INOIS input configuration file.')
def run(input_file):
    """The entry point class for the INOIS hashing application."""

    logging.info("Application Started")
    print(Banner.TEXT)
    config = ConfigService.initialize_config(input_file=input_file)
    FileService.validate_files(config)
    HashService.hash_files(config)



if __name__ == "__main__":
    run()

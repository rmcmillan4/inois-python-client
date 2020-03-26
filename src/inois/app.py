import click
import logging
from inois.utils.banner import Banner
from inois.services.config_service import ConfigService

logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s', filename='inois.log', level=logging.DEBUG)

@click.command()
@click.option('--input_file', prompt='input file', help='Path to the INOIS input configuration file.')
#@click.option('--username', prompt='username', help='Azure Active Directory Username')
def run(input_file):
    """The entry point class for the INOIS hashing application."""

    logging.info("Application Started")
    print(Banner.TEXT)
    config = ConfigService.initialize_config(input_file=input_file)


if __name__ == "__main__":
    run()

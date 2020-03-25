import click
from inois.utils.banner import Banner
from inois.services.config_service import ConfigService


@click.command()
@click.option('--input_file', prompt='input file', help='Path to the INOIS input configuration file.')
#@click.option('--username', prompt='username', help='Azure Active Directory Username')
def run(input_file):
    """The entry point class for the INOIS hashing application."""

    print(Banner.TEXT)
    config = ConfigService.initialize_config(input_file=input_file)


if __name__ == "__main__":
    run()

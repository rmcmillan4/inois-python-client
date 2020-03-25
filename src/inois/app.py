import click
from inois.utils.banner import Banner

@click.command()
@click.option('--input', prompt='input file', default='input.txt', help='Path to the INOIS input configuration file.')
@click.option('--username', prompt='username', help='Azure Active Directory Username')
def run(input, username):
    """The entry point class for the INOIS hashing application."""

    print(Banner.text)
    print(username)


if __name__ == "__main__":
    run()

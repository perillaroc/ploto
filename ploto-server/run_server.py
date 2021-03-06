# coding=utf-8
import click


@click.command()
@click.option('-c', '--config-file', help='config file path')
def runserver(config_file):
    """
    DESCRIPTION
        Run ploto server.
    """

    from ploto_server.app import create_app
    app = create_app(config_file)

    app.run(
        host=app.config['server_config']['broker']['host']['ip'],
        port=app.config['server_config']['broker']['host']['port']
    )


if __name__ == '__main__':
    runserver()

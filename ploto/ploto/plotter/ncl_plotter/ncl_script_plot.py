import subprocess
import click
import json


@click.command()
@click.option('--param', help='json param string')
def ncl_script_plot(param):
    param_object = json.loads(param)
    ncl_params = param_object['ncl_params']
    ncl_script = param_object['ncl_script_path']

    ncl_result = subprocess.run(
        ['/bin/bash', '-i', '-c', 'ncl {ncl_params} {ncl_script}'.format(
            ncl_params=ncl_params,
            ncl_script=ncl_script
        )]
    )
    # print(ncl_result.stdout)
    # print(ncl_result.stderr)


if __name__ == "__main__":
    ncl_script_plot()

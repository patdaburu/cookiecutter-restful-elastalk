#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: {{cookiecutter.package_name}}.cli
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

This module defines the command-line interface (CLI) for the
{{cookiecutter.package_name}} package.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.
"""
import logging
import os
from pathlib import Path
import sys
import traceback
from typing import Iterable
import click
from .__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG
}  #: a mapping of `verbose` option counts to logging levels

PACKAGE_NAME = __name__.split('.')[0]  #: the name of the package


class Info(object):
    """
    This is an information object that can be used to pass data between CLI
    functions.
    """
    def __init__(self):  # Note that this object must have an empty constructor.
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
pass_info = click.make_pass_decorator(
    Info,
    ensure=True
)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option('--verbose', '-v', count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info,
        verbose: int):
    """
    This is the txauthor API service.  You can use gunicorn or another
    production host to run the service, but this command-line interface provides
    some other handy help and utilities.
    """
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f'Verbose logging is enabled. '
                f'(LEVEL={logging.getLogger().getEffectiveLevel()})',
                fg='yellow'
            )
        )
    info.verbose = verbose


@cli.command()
@click.option('--flask-env', '-f', 'flask_env',
              type=click.Choice([
                  'production',
                  'staging',
                  'development',
                  'testing'
              ]),
              default='production',
              help="Set the Flask environment.")
@click.option('--es-host', multiple=True,
              help='Identify Elasticsearch hosts.')
@click.option('--static-folder', '-s', 'static_folder',
              type=click.Path(exists=True),
              default=None,
              help="Set the static file path.")
@click.option('--host', '-h', type=str, default='127.0.0.1',
              help='Set the host to listen.')
@click.option('--port', '-p', type=int, default=4000,
              help='Set the port to listen.')
@click.option('--workers', '-w', type=int, default=4,
              help='Indicate the number of worker processes.')
@pass_info
def run(_: Info,
        flask_env: str,
        es_host: Iterable[str],
        static_folder: str,
        host: str,
        port: int,
        workers: int):
    """
    Run the server.
    """
    if flask_env:
        os.environ['FLASK_ENV'] = flask_env
    if es_host:
        os.environ['ES_HOST'] = ','.join(es_host)
    if static_folder:
        os.environ['STATIC_FOLDER'] = static_folder
    cmd = (
        f"gunicorn -w {workers} "
        f"-b {host}:{port} "
        f"{{cookiecutter.package_name}}.app:app"
    )
    click.echo(click.style(cmd, fg='blue'))
    os.system(cmd)


@cli.command()
def version():
    """
    Get the version.
    """
    click.echo(click.style(f'{__version__}', bold=True))
